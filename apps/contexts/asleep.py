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
        self.listen_state(self.on_if_presleep, "light.monitor", new = "off")

        self.Utils = self.get_app("Utilities")

    def on_if_presleep(self, entity, attribute, old, new, kwargs):
        if self.get_state("input_select.context") == "Pre-sleep":
            self.set_state("input_select.context", state = "Asleep")

    def on(self, entity, attribute, old, new, kwargs):
        self.log("Starting good-night script")

        self.Utils.light_setter("light.monitor", fade = 5, brightness = 0)
        self.Utils.light_setter("light.bathroom_2", fade = 5, brightness = 0)

        self.turn_off("media_player.pioneer")
        self.turn_off("input_boolean.circadian")
        self.turn_off("input_boolean.sunrise")
        self.turn_off("input_boolean.carpediem")

        for i in range(0, 6):
            if self.get_state("light.monitor") == "on":
                self.log("Monitor is on, sleeping for 2s")
                time.sleep(2)
            else:
                self.log("Monitor turned off, continuing")
                break

        self.call_service("light/turn_off", entity_id = "all")

        for i in range(0, 5):
            if self.get_state("light.all") == "on":
                self.log("All lights not yet off, repeating")
                self.call_service("light/turn_off", entity_id = "all")
                time.sleep(2)

        self.log("Finished good-night script, good night!")
