import appdaemon.plugins.hass.hassapi as hass
import circadiangen
import time
import datetime
from time import sleep
import globals as g

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
        self.listen_state(self.leaving, "input_select.context", old = "Cozy")

        self.Utils = self.get_app("Utilities")

    def on(self, entity, attribute, old, new, kwargs):
        self.turn_on("switch.vindue")
        self.turn_on("switch.seng")
        g.c_colortemp = 2300

        lights = [
            ["light.loft_3", 1],
            ["light.reol_3", 5],
            ["light.gang_2", 5],
            ["light.bathroom_2", 10],
            ["light.arbejds_2", 5]
        ]

        for light in lights:
            self.Utils.light_setter(light[0], brightness = 0, fade = light[1])

        self.Utils.light_setter("light.monitor", brightness=125, fade=10)

        self.turn_off("input_boolean.circadian")
        self.turn_on("media_player.pioneer")

        sleep(2)

        n = 0

        '''
        for i in range(0, 10):
            if self.get_state("input_select.context") == "Cozy":
                if self.get_state("media_player.pioneer") == "on":
                    if n < 2:
                        self.call_service("media_player/volume_set",
                                          entity_id = "media_player.pioneer",
                                          volume_level = "0.32")
                        sleep(1)
                        self.call_service("media_player/select_source",
                                          entity_id = "media_player.pioneer",
                                          source = "CHROME")
                        sleep(1)
                        n += 1
                else:
                    self.call_service("media_player/select_source",
                                      entity_id = "media_player.pioneer",
                                      source = "CHROME")
                    self.log("Pioneer not on, re-powering and sleeping for 3s")
                    sleep(3)
        '''

        self.log("Finished init of cozy")


    def leaving(self, entity, attribute, old, new, kwargs):
        self.turn_off("media_player.pioneer")
        self.turn_off("switch.vindue")
        self.turn_off("switch.seng")
