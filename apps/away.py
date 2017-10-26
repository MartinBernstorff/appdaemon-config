import appdaemon.appapi as appapi
import circadiangen
import time
import datetime

#
# Carpediem app
#
# Args:
#   switch: The switch that initializes the script
#   factor: the input_select that determines the factor length

class Away(appapi.AppDaemon):
    def initialize(self):
        self.listen_state(self.on, "input_select.context", new = "Away")

    def on(self, entity, attribute, old, new, kwargs):
        self.log("Starting Away script")

        # Prevent Normal from firing
        self.global_vars["door_opened_recently"] = 1
        if self.get_state("input_select.context") == "Away":
            self.turn_off("group.all_lights")
            self.turn_off("media_player.pioneer")
        if self.get_state("input_select.context") == "Away":
            self.turn_off("input_boolean.sunrise")
            self.turn_off("input_boolean.carpediem")

        if self.get_state("input_select.context") == "Away":
            self.turn_off("group.all_lights")
            time.sleep(2)

        if self.get_state("input_select.context") == "Away":
            self.turn_off("group.all_lights")
            time.sleep(2)

        self.log("Away script execution finished!")
