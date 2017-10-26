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

class PreSleep(appapi.AppDaemon):
    def initialize(self):
        self.log("Initializing {} with switch: {}".format(__name__, self.args["switch"]))

        self.listen_state(self.on, "input_select.context", new = "Pre-sleep")

    def on(self, entity, attribute, old, new, kwargs):
        self.log("Running pre-sleep actions")
        self.turn_off("group.all_lights")
        self.turn_on("light.monitor", xy_color = [0.6756, 0.3202], brightness = "60")
        self.turn_on("light.bathroom", xy_color = [0.6756, 0.3202], brightness = "0")
