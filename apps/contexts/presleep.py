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

class PreSleep(hass.Hass):
    def initialize(self):
        self.log("Initializing {} with switch: {}".format(__name__, self.args["switch"]))

        self.listen_state(self.on, "input_select.context", new = "Pre-sleep")

        self.Utils = self.get_app("Utilities")

    def on(self, entity, attribute, old, new, kwargs):
        self.log("Running pre-sleep actions")
        lights = ["light.loft_2",
                  "light.gang",
                  "light.reol_2"
                  ]
        for light in lights:
            self.Utils.light_setter(light, fade = 2, brightness = 0)
            time.sleep(1)

        self.turn_off("group.all_switches")

        self.Utils.light_setter("light.bathroom_2", brightness = 1, xy_color = [0.6948, 0.3002], fade = 10)
        self.Utils.light_setter("light.monitor", brightness = 60, xy_color = [0.6948, 0.3002], fade = 10)
