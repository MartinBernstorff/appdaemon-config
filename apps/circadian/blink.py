import appdaemon.plugins.hass.hassapi as hass
import time
import datetime
from rgb_xy import Converter
import globals as g

conv = Converter()

"""
Blink app

Args:
switch: The switch that initializes the script
light: The light that's used for sunrise


"""


class Blink(hass.Hass):
    def initialize(self):
        self.log("Initializing blink")
        self.switch = self.args["switch"] # The switch to turn on/off the sunrise

        self.light = "light.monitor" # The light to act as sun

        self.listen_state(self.run_blink, self.args["switch"], new="on") # Callback for testing

        self.set_alarm()

        #self.run_blink()

        # Set alarm daily, or when settings have changed
        runtime = datetime.time(19, 0, 0)
        self.run_daily(self.set_alarm, runtime)
        self.listen_state(self.set_alarm, "input_select.blink_hour")
        self.listen_state(self.set_alarm, "input_select.blink_minute")
        self.listen_state(self.set_alarm, "input_boolean.blink_alarm")

        self.Utils = self.get_app("Utilities")

    def set_alarm(self, entity="", attribute="", old="", new="", kwargs=""):
        self.alarm = None
        if self.get_state("input_boolean.blink_alarm") == "on":
            self.hour = self.get_state("input_select.blink_hour") # hour here
            self.minute = self.get_state("input_select.blink_minute")# minute her
            self.alarm_time = self.parse_time("{}:{}:00".format(self.hour, self.minute))

            self.alarm = self.run_daily(self.launch, self.alarm_time,
                                        constrain_days="mon,tue,wed,thu,fri")
            self.log("Set alarm to {}".format(self.info_timer(self.alarm)[0]))
        elif self.get_state("input_boolean.blink_alarm") == "off":
            self.cancel_timer(self.alarm)
            self.log("Cancelled alarm timer")

    def launch(self, entity="", attribute="", old="", new="", kwargs=""):
        if self.get_state(self.args["switch"]) == "off":
            self.turn_on(self.args["switch"])
        else:
            self.turn_off(self.args["switch"])
            self.turn_on(self.args["switch"])

    def run_blink(self, entity="", attribute="", old="", new="", kwargs=""):
        self.turn_on("light.monitor", kelvin=5000)
        self.turn_off("light.monitor")

        self.i = 0
        for i in range(5):
            self.i += 5
            self.run_in(self.blink_light, self.i)

    def blink_light(self, entity="", attribute="", old="", new="", kwargs=""):
        self.log("Blinked!")
        self.turn_on("light.monitor", flash = "short", brightness = 2)
        self.turn_off("light.monitor")
