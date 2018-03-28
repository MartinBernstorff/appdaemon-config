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

class Sleep(hass.Hass):
    def initialize(self):
        self.log("Initializing {} with switch: {}".format(__name__, self.args["switch"]))

        self.listen_state(self.on, "input_select.context", new = "Sleep")

        self.listen_event(self.button_single, "click", entity_id = "binary_sensor.switch_158d0001a1f52f", click_type = "single")

        self.utils = self.get_app("utilities")

    def button_single(self, entity, attribute, old, new="", kwargs=""):
        if self.get_state("input_select.context") == "Sleep":
            self.log("Toggling night-light")

            if self.get_state("light.monitor") == "on":
                self.turn_off("light.monitor")
            elif self.get_state("light.monitor") == "off":
                self.turn_on("light.monitor", xy_color = [0.6948, 0.3002], brightness = "60")

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
