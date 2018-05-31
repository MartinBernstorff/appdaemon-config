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
        self.setstate("light.hallway", 50, 1, [0.5267, 0.4132])
        self.turn_off("light.ikea_loft")
        self.setstate("light.monitor", 180, 1, [0.5267, 0.4132])
        self.setstate("ight.color_temperature_light_1", 180, 1, [0.3823, 0.3708])

    def setstate(self, lt, bness, fade, color=""):
        self.modulator = 1

        self.log("Set " + lt + " to fade in " + str(fade * self.modulator) + "s")

        if color != "":
            self.turn_on(lt, brightness = bness, transition = self.modulator * fade, xy_color = color)
        else:
            self.turn_on(lt, brightness = bness, transition = self.modulator * fade)
