import time
import datetime
import appdaemon.plugins.hass.hassapi as hass
import globals as g

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

        self.utils = self.get_app("Utilities")

    def carpe_diem(self, entity, attribute, old, new, kwargs):
        if self.get_state("device_tracker.iphonevanmieke") == "home":
            self.turn_on("input_boolean.carpemieke")
            return

        self.turn_off("input_boolean.circadian") #Turn off circadian temporarily
        self.turn_off("input_boolean.sunrise") #Turn off sunrise if it's stil on

        g.c_colortemp = 3000
        g.c_brightness = 655

        """ A list of lists containing:
        Entity id, delay, fade duration
        """

        lights = [
            ["light.monitor", 1, 10],
            ["light.bathroom_2", 1, 3],
            ["light.color_temperature_light_1", 20, 20],
            ["light.ikea_loft", 45, 20],
            ["light.hallway_2", 5, 80],
        ]

        duration = 0

        for light in lights:
            self.run_in(self.light_controller,
                        light[1] * self.modulator,
                        lt=light[0],
                        fade=light[2])

            light_duration = (light[1] + light[2]) * self.modulator

            if light_duration > duration:
                duration = light_duration * self.modulator

        self.run_in(self.finished, duration + 10)

    def carpe_mieke(self, entity, attribute, old, new, kwargs):
        self.turn_off("input_boolean.circadian") #Turn off circadian temporarily
        self.turn_off("input_boolean.sunrise") #Turn off sunrise if it's stil on
        self.log("Starting carpe-Mieke")

        g.c_colortemp = 2000
        g.c_brightness = 655

        """ A list of lists containing:
        Entity id, delay, fade duration
        """

        lights = [
            ["light.monitor", 1, 30],
            ["light.bathroom_2", 1, 20],
            ["light.color_temperature_light_1", 60, 180],
            ["light.ikea_loft", 210, 300],
            ["light.hallway_2", 60, 300],
        ]

        duration = 0  * self.modulator

        for light in lights:
            self.run_in(self.light_controller,
                        light[1] * self.modulator,
                        lt=light[0],
                        fade=light[2],
                        switch="input_boolean.carpemieke")

            light_duration = light[1] + light[2]

            if light_duration > duration:
                duration = light_duration * self.modulator

        self.run_in(self.finished, duration)

    def light_controller(self, kwargs):
        if "switch" in kwargs:
            switch = kwargs["switch"]
        else:
            switch = self.args["switch"]

        self.setstate(lt=kwargs["lt"],
                      brightness=g.c_brightness,
                      fade=kwargs["fade"],
                      color=g.c_colortemp,
                      switch=switch)

    def setstate(self, lt, brightness, fade, switch, color=""):
        if self.get_state(switch) == "on":
            self.log("Set " + lt + " to fade in over " + str(fade * self.modulator) + "s with \n     Brightness: {}\n     Kelvin: {}".format(brightness, color))

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
        if self.get_state(self.args["switch"]) == "on":
            self.turn_on("input_boolean.circadian") #Turn back on circadian
            time.sleep(2)
            self.set_state("input_select.context", state = "Normal")
            self.reset()
        elif self.get_state("input_boolean.carpemieke") == "on":
            self.set_state("input_select.context", state = "Cozy")
            self.reset()
        else:
            self.log("Switch is off, not running finished")
