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

    def on(self, entity, attribute, old, new, kwargs):
        self.log("Running pre-sleep actions")
        self.turn_on("light.monitor", xy_color = [0.6948, 0.3002], brightness = "60")
        self.turn_on("light.bathroom_2", xy_color = [0.6948, 0.3002], brightness = "1")

        lights = ["color_temperature_light_1",
                  "color_temperature_light_1_2", "fishbowl", "gateway_light_286c07f0bbf5",
                  "hallway", "hallway_2", "ikea_loft"]
        for light in lights:
            self.turn_off("light.{}".format(light))
