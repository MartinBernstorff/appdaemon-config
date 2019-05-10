import appdaemon.plugins.hass.hassapi as hass
import circadiangen
import time
import datetime
import globals as g

#
# Carpediem app
#
# Args:
#   switch: The switch that initializes the script
#   factor: the input_select that determines the factor length

class CarpeMieke(hass.Hass):
    def initialize(self):
        self.log("Initializing {} with switch: {}".format(__name__, self.args["switch"]))

        self.listen_state(self.on_from_boolean, "input_boolean.carpemieke", new = "on")

        self.utils = self.get_app("utilities")

        self.modulator = 1

    def on(self):
        self.log("Starting carpe Mieke")

        self.turn_off("input_boolean.circadian") #Turn off circadian temporarily
        self.turn_off("input_boolean.sunrise") #Turn off sunrise if it's stil on

        g.c_colortemp = 2000
        g.c_brightness = 655
        g.persistent_hallway_light = True

    def reset(self, entity="", attribute="", old="", new="", kwargs=""):
        self.turn_off(self.args["switch"])

    def on_from_boolean(self, entity, attribute, old, new, kwargs):
        self.on()

        """ A list of lists containing:
        Entity id, delay, fade duration
        """

        lights = [
            ["light.monitor", 2, 30],
            ["light.bathroom_2", 2, 20],
            ["light.reol_2", 60, 180],
            ["light.loft_2", 210, 300],
            ["light.gang", 60, 300],
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

        self.set_state("input_select.context", state = "Carpe Mieke")

        self.reset()
        self.log("Finished carpe mieke!")

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
