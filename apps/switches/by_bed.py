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

# Button B

class ByBed(hass.Hass):
    def initialize(self):
        self.log("Initializing {}".format(__name__))

        self.listen_event(self.single_click, "click", entity_id = "binary_sensor.switch_158d0001a1f52f", click_type = "single")
        self.listen_event(self.double_click, "click", entity_id = "binary_sensor.switch_158d0001a1f52f", click_type = "double")
        self.listen_event(self.long_click_press, "click", entity_id = "binary_sensor.switch_158d0001a1f52f", click_type = "long_click_press")

    def single_click(self, entity, attribute, old, new="", kwargs=""):
        # Define context-specific actions
        # Double-click is moving forward in circadian contexts
        self.log("Single-click!")
        self.log("Context is {}, moving forward".format(self.get_state("input_select.context")))
        if self.get_state("input_select.context") == "Normal":
            self.set_state("input_select.context", state="Pre-sleep")
        elif self.get_state("input_select.context") == "Pre-sleep":
            self.set_state("input_select.context", state="Asleep")
        elif self.get_state("input_select.context") == "Asleep":
            self.turn_on("input_boolean.carpediem")
        self.log("New context is {}".format(self.get_state("input_select.context")))

    def double_click(self, entity, attribute, old, new="", kwargs=""):
        self.log("Double-click")

    def long_click_press(self, entity, attribute, old, new="", kwargs=""):
        self.log("Long_click_press!")
        self.log("Context is {}, moving backwards".format(self.get_state("input_select.context")))
        if self.get_state("input_select.context") == "Normal":
            self.set_state("input_select.context", state="Asleep")
        elif self.get_state("input_select.context") == "Pre-sleep":
            self.set_state("input_select.context", state="Normal")
            self.turn_on("")
        elif self.get_state("input_select.context") == "Asleep":
            if self.get_state("input_boolean.carpediem") == "off":
                self.set_state("input_select.context", state="Pre-sleep")
            elif self.get_state("input_boolean.carpediem") == "on":
                self.turn_off("input_boolean.carpediem")
                self.turn_on("input_boolean.good_night")
        else:
            self.set_state("input_select.context", state="Normal")
        self.log("New context is {}".format(self.get_state("input_select.context")))
