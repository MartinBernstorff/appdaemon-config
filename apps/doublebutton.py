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

class DoubleButton(hass.Hass):
    def initialize(self):
        self.log("DoubleButton is working!")
        self.listen_event(self.right, "click", entity_id = "binary_sensor.wall_switch_right_158d000183f392", click_type = "single")
        self.listen_event(self.both, "click", entity_id = "binary_sensor.wall_switch_both_158d000183f392", click_type = "both")

    def right(self, entity, attribute, old, new="", kwargs=""):
        # Define context-specific actions
        if self.get_state("input_select.context") == "Normal":
            if self.get_state("light.bathroom") != "on":
                self.turn_on("light.bathroom", transition = 0.5, xy_color = self.global_vars["c_colortemp"], brightness = self.global_vars["c_brightness"] * 1.4)
            else:
                self.turn_off("light.bathroom")
        elif self.get_state("input_select.context") == "Pre-sleep":
            if self.get_state("light.bathroom") == "off":
                self.turn_on("light.bathroom", xy_color = [0.6948, 0.3002], brightness = "0")
            else:
                self.turn_off("light.bathroom")
        elif self.get_state("input_select.context") == "Cozy":
            if self.get_state("light.bathroom") == "off":
                self.turn_on("light.bathroom", xy_color = [0.52, 0.42], brightness = "150")
            else:
                self.turn_off("light.bathroom")
        else: #And if no context is recognized
            if self.get_state("light.bathroom") == "on":
                self.turn_off("light.bathroom")
            if self.get_state("light.bathroom") == "off":
                self.turn_on("light.bathroom")

    def both(self, entity, attribute, old, new="", kwargs=""):
        if self.get_state("input_select.context") != "Away":
            self.set_state("input_select.context", state = "Away")
        else:
            self.global_vars["door_opened_recently"] = 1
            self.set_state("input_select.context", state = "Normal")
