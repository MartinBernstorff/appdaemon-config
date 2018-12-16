import appdaemon.plugins.hass.hassapi as hass
import circadiangen
import time
import datetime

#
# Carpediem app
#
# Args:
#   switch: The switch that initializes the script
#   factor: the input_select that determines the factor length

class Cozy(hass.Hass):
    def initialize(self):
        self.log("Initializing {} with switch: {}".format(__name__, self.args["switch"]))

        self.listen_state(self.on, "input_select.context", new = "Cozy")

    def on(self, entity, attribute, old, new, kwargs):
        self.setstate("light.hallway_2", 1, 1, 2300)
        self.turn_off("light.ikea_loft")
        self.setstate("light.monitor", 125, 1, 2300)
        self.setstate("light.color_temperature_light_1", 63, 1, 2300)

    def setstate(self, lt, bness, fade, color=""):
        self.modulator = 1

        self.log("Set " + lt + " to fade in " + str(fade * self.modulator) + "s")

        if color != "":
            self.turn_on(lt, brightness = bness, transition = self.modulator * fade, kelvin = color)
        else:
            self.turn_on(lt, brightness = bness, transition = self.modulator * fade)
