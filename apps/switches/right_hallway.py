import appdaemon.plugins.hass.hassapi as hass
import circadiangen
import time
import datetime
import globals as g

#
# Carpediem app
#
# Args:
#   switch: The switch that initializes the script
#   factor: the input_select that determines the factor length

# Button A

class RightHallway(hass.Hass):
    def initialize(self):
        self.log("SingleButton_A, at your service.")
        self.listen_event(self.single_click, "xiaomi_aqara.click", entity_id = "binary_sensor.switch_158d000201a251", click_type = "single")
        self.listen_event(self.double_click, "xiaomi_aqara.click", entity_id = "binary_sensor.switch_158d000201a251", click_type = "double")
        self.listen_event(self.long_click_press, "xiaomi_aqara.click", entity_id = "binary_sensor.switch_158d000201a251", click_type = "long_click_press")

    def single_click(self, entity, attribute, old, new="", kwargs=""):
        self.log("Right-hallway pressed!")
        # Define context-specific actions
        if self.get_state("input_select.context") == "Normal":
            if self.get_state("light.bathroom_2") != "on":
                self.turn_on("light.bathroom_2", transition = 0.5, kelvin = g.c_colortemp, brightness = g.c_brightness * 1.4)
            else:
                self.turn_off("light.bathroom_2")
        elif self.get_state("input_select.context") == "Pre-sleep":
            if self.get_state("light.bathroom_2") == "off":
                self.turn_on("light.bathroom_2", xy_color = [0.6948, 0.3002], brightness = "1")
            else:
                self.turn_off("light.bathroom_2")
        elif self.get_state("input_select.context") == "Asleep":
            if self.get_state("light.bathroom_2") == "off":
                self.turn_on("light.bathroom_2", xy_color = [0.6948, 0.3002], brightness = "1")
            else:
                self.turn_off("light.bathroom_2")
        elif self.get_state("input_select.context") == "Cozy":
            if self.get_state("light.bathroom_2") == "off":
                self.turn_on("light.bathroom_2", xy_color = [0.52, 0.42], brightness = "150")
            else:
                self.turn_off("light.bathroom_2")
        else: #And if no context is recognized
            if self.get_state("light.bathroom_2") == "on":
                self.turn_off("light.bathroom_2")
            if self.get_state("light.bathroom_2") == "off":
                self.turn_on("light.bathroom_2")

    def double_click(self, entity, attribute, old, new="", kwargs=""):
        self.log("Right-hallway double-clicked!")

    def long_click_press(self, entity, attribute, old, new="", kwargs=""):
        self.log("Right-hallway long_pressed!")
        self.log("{} turned {}".format(entity, new))
        if self.get_state("input_select.context") != "Pre-sleep":
            self.set_state("input_select.context", state="Pre-sleep")
