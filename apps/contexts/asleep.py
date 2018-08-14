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

class Asleep(hass.Hass):
    def initialize(self):
        self.log("Initializing {} with switch: {}".format(__name__, self.args["switch"]))

        self.listen_state(self.on, "input_select.context", new = "Asleep")

        self.utils = self.get_app("utilities")

    def on(self, entity, attribute, old, new, kwargs):
        self.log("Starting good-night script")
        self.turn_off("group.all_lights")
        self.turn_off("media_player.pioneer")
        self.turn_off("input_boolean.circadian")
        self.turn_off("input_boolean.sunrise")
        self.turn_off("input_boolean.carpediem")
        self.turn_off("group.all_lights")
        time.sleep(2)
        self.turn_off("group.all_lights")
        self.turn_off("media_player.pioneer")
        self.turn_off("input_boolean.circadian")
        self.turn_off("input_boolean.sunrise")
        self.turn_off("input_boolean.carpediem")
        self.turn_off("group.all_lights")
