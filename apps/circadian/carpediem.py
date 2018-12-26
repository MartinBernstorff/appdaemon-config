import time
import datetime
import appdaemon.plugins.hass.hassapi as hass

#
# Carpediem app
#
# Args:
#   switch: The switch that initializes the script

class CarpeDiem(hass.Hass):
    def initialize(self):
        self.log("Initializing carpe diem with switch: " + self.args["switch"])
        #Setup the switch object
        switch = self.args["switch"]

        #Reset switch to off
        self.reset()

        # Register callback
        self.on_default = self.listen_state(self.carpe_diem, switch, new="on")
        self.on_mieke = self.listen_state(self.carpe_mieke, "input_boolean.carpemieke", new="on")

        #Reset the switch at 20:00 each day
        self.time = datetime.time(20, 0, 0)
        self.run_daily(self.reset, self.time)

        self.modulator = 1

    def carpe_diem(self, entity, attribute, old, new, kwargs):
        self.turn_off("input_boolean.circadian") #Turn off circadian temporarily
        self.turn_off("input_boolean.sunrise") #Turn off sunrise if it's stil on

        self.global_vars["c_colortemp"] = 3000

        """ A list of lists containing:
        Entity id, delay, fade duration
        """

        lights = [
            ["light.monitor", 1, 10],
            ["light.bathroom_2", 1, 3],
            ["light.color_temperature_light_1", 10, 20],
            ["light.ikea_loft", 30, 15],
            ["light.hallway_2", 30, 15],
        ]

        duration = 0

        for light in lights:
            self.run_in(self.light_controller, light[1], lt=light[0],
                        fade=light[2])

            light_duration = light[1] + light[2]

            if light_duration > duration:
                duration = light_duration

        self.run_in(self.finished, duration)

    def carpe_mieke(self, entity, attribute, old, new, kwargs):
        self.turn_off("input_boolean.circadian") #Turn off circadian temporarily
        self.turn_off("input_boolean.sunrise") #Turn off sunrise if it's stil on
        self.log("Starting carpe-Mieke")

        self.global_vars["c_colortemp"] = 2500

        """ A list of lists containing:
        Entity id, delay, fade duration
        """

        lights = [
            ["light.monitor", 1, 30],
            ["light.bathroom_2", 1, 20],
            ["light.color_temperature_light_1", 30, 180],
            ["light.ikea_loft", 210, 300],
            ["light.hallway_2", 60, 300],
        ]

        duration = 0

        for light in lights:
            self.run_in(self.light_controller, light[1], lt=light[0],
                        fade=light[2], switch="input_boolean.carpemieke")

            light_duration = light[1] + light[2]

            if light_duration > duration:
                duration = light_duration

        self.run_in(self.finished, duration)

    def light_controller(self, kwargs):
        if kwargs["switch"] is None:
            switch = self.args["switch"]
        else:
            switch = kwargs["switch"]

        self.setstate(lt=kwargs["lt"],
                      brightness=self.global_vars["c_brightness"],
                      fade=kwargs["fade"],
                      color=self.global_vars["c_colortemp"],
                      switch=switch)

    def setstate(self, lt, brightness, fade, switch, color=""):
        if self.get_state(switch) == "on":
            self.log("Set " + lt + " to fade in over " + str(fade * self.modulator) + "s")

            if self.get_state(switch) == "on":
                if color != "":
                    self.turn_on(lt, brightness=brightness, transition=self.modulator * fade, kelvin=color)
                else:
                    self.turn_on(lt, brightness=brightness, transition=self.modulator * fade)

            if self.get_state(switch) == "on":
                time.sleep(self.modulator * fade)
        else:
            self.log("Switch turned off, terminating")

    def reset(self, entity="", attribute="", old="", new="", kwargs=""):
        self.turn_off(self.args["switch"])
        self.turn_off("input_boolean.carpemieke")

    def finished(self, entity="", attribute="", old="", new="", kwargs=""):
        self.turn_on("input_boolean.circadian") #Turn back on circadian
        self.set_state("input_select.context", state = "Normal")
        self.reset()
