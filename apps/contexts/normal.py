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

class Normal(hass.Hass):
    def initialize(self):
        self.log("Initializing {} with switch: {}".format(__name__, self.args["switch"]))

        self.listen_state(self.on, "input_select.context", new = "Normal")


    def on(self, entity, attribute, old, new, kwargs):
        if self.get_state("input_boolean.circadian") == "on":
            self.log("Circadian switch on, updating lights to Normal context")
            self.brightness = self.global_vars["c_brightness"]
            self.xy_color = self.global_vars["c_colortemp"]

            self.log("Updating lights quickly,\n    Color: {}\n    Brightness: {}".format(self.xy_color, self.brightness))
            self.turn_on("light.ikea_loft", transition = 1, xy_color = self.xy_color, brightness = 0.6 * self.brightness)
            self.turn_on("ight.color_temperature_light_1", transition = 1, xy_color = self.xy_color, brightness = 0.4 * self.brightness)
            self.turn_on("light.monitor", transition = 1, xy_color = self.xy_color, brightness = 1.6 * self.brightness)
        else:
            # self.log("Circadian switch is off, lights not updated")
            pass