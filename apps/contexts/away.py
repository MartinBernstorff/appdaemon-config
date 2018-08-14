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

class Away(hass.Hass):
    def initialize(self):
        self.listen_state(self.on, "input_select.context", new = "Away")

    def on(self, entity, attribute, old, new, kwargs):
        if self.get_state("input_select.context") == "Away":
            self.log("Starting Away script")
        else:
            self.log("Aborting Away script, input_select.context == {}".format(self.get_state("input_select.context")))

        # Prevent Normal from firing
        self.global_vars["door_opened_recently"] = 1
        if self.get_state("input_select.context") == "Away":
            self.turn_off("group.all_lights")
            self.turn_off("media_player.pioneer")
            self.log("Phase 1 complete")

        if self.get_state("input_select.context") == "Away":
            self.turn_off("input_boolean.sunrise")
            self.turn_off("input_boolean.carpediem")
            self.log("Phase 2 complete")

        self.log("Away script execution finished!")
