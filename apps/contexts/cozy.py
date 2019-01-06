import appdaemon.plugins.hass.hassapi as hass
import circadiangen
import time
import datetime
from time import sleep

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
        self.turn_off("light.ikea_loft")
        self.setstate("light.hallway_2", 1, 1, 2300)
        self.setstate("light.monitor", 125, 1, 2300)
        self.setstate("light.color_temperature_light_1", 50, 1, 2300)
        self.turn_on("media_player.pioneer")

        sleep(10)
        self.call_service("media_player/select_source",
                          entity_id = "media_player.pioneer",
                          source = "CHROME")

        for i in range(0, 5):
            self.call_service("media_player/volume_set",
                              entity_id = "media_player.pioneer",
                              volume_level = "0.6648")
            sleep(3)
            self.call_service("media_player/select_source",
                              entity_id = "media_player.pioneer",
                              source = "CHROME")
            sleep(3)

    def setstate(self, lt, bness, fade, color=""):
        self.modulator = 1

        self.log("Set " + lt + " to fade in " + str(fade * self.modulator) + "s with parameters {} {}".format(bness, color))

        if color != "":
            self.turn_on(lt, brightness = bness, transition = self.modulator * fade, kelvin = color)
        else:
            self.turn_on(lt, brightness = bness, transition = self.modulator * fade)
