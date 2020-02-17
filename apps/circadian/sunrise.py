import appdaemon.plugins.hass.hassapi as hass
import time
import datetime
from rgb_xy import Converter
import globals as g

conv = Converter()

"""
Sunrise app

Args:
switch: The switch that initializes the script
light: The light that's used for sunrise


"""


class Sunrise(hass.Hass):
    def initialize(self):
        self.log("Initializing sunrise")
        self.switch = self.args["switch"] # The switch to turn on/off the sunrise

        self.light = "light.monitor" # The light to act as sun

        self.listen_state(self.rise_default, self.args["switch"], new="on") # Callback for testing

        self.set_alarm()

        self.listen_state(self.set_alarm, "input_select.sunrise_hour")
        self.listen_state(self.set_alarm, "input_select.sunrise_minute")
        self.listen_state(self.set_alarm, "input_boolean.sunrise_alarm")

        self.Utils = self.get_app("Utilities")

    def set_alarm(self, entity="", attribute="", old="", new="", kwargs=""):
        self.alarm = None
        if self.get_state("input_boolean.sunrise_alarm") == "on":
            self.hour = self.get_state("input_select.sunrise_hour") # hour here
            self.minute = self.get_state("input_select.sunrise_minute")# minute her
            self.alarm_time = self.parse_time("{}:{}:00".format(self.hour, self.minute))

            self.alarm = self.run_daily(self.launch, self.alarm_time,
                                        constrain_days="mon,tue,wed,thu,fri")
            self.log("Set alarm to {}".format(self.info_timer(self.alarm)[0]))
        elif self.get_state("input_boolean.sunrise_alarm") == "off":
            self.cancel_timer(self.alarm)
            self.log("Cancelled alarm timer")

    def launch(self, entity="", attribute="", old="", new="", kwargs=""):
        if self.get_state(self.args["switch"]) == "off":
            self.turn_on(self.args["switch"])
        else:
            self.turn_off(self.args["switch"])
            self.turn_on(self.args["switch"])

    def rise_default(self, entity="", attribute="", old="", new="", kwargs=""):
        self.modifier = 1
        self.log("Rise_default is running with switch {switch}, light {light} and modifier {modifier}".format(switch=self.switch, light=self.light, modifier = self.modifier))
        self.Utils.light_setter(switch=self.switch, lt=self.light, brightness=1, fade=10, kelvin=3000)
        self.Utils.light_setter(switch=self.switch, lt=self.light, brightness=255, fade=290, kelvin=5000)

    #######################
    # Different sequences #
    #######################

    def red_only(self):
        self.condseq_on(switch=self.switch, entity=self.light, brightness=1, t_fade=1, color=[0.674, 0.322])
        self.condseq_on(switch=self.switch, entity=self.light, brightness=10, t_fade=1800, color=[0.674, 0.322])
        self.condseq_on(switch=self.switch, entity=self.light, brightness=100, t_fade=1800, color=[0.5268, 0.4133])
        self.turn_on("input_boolean.circadian")

    def natural(self, *args, **kwargs):
        self.log("Natural sunrise is running with switch {switch}, light {light} and modifier {modifier}".format(switch=self.switch, light=self.light, modifier = self.modifier))
        # self.condseq_on(switch=self.switch, entity=self.light, brightness=1, t_fade=1, color=conv.rgb_to_xy(255, 0, 0))
        self.condseq_on(switch=self.switch, entity="light.monitor", brightness=1, t_fade=1, color=3000)
        self.condseq_on(switch=self.switch, entity="light.monitor", brightness=1, t_fade=500, color=3000)
        self.condseq_on(switch=self.switch, entity="light.monitor", brightness=15, t_fade=400, color=3000)
        self.condseq_on(switch=self.switch, entity=self.light, brightness=1, t_fade=1, color=3000)
        self.condseq_on(switch=self.switch, entity=self.light, brightness=1, t_fade=899, color=3000)
        self.condseq_on(switch=self.switch, entity=self.light, brightness=255, t_fade=900, color=3000)
        self.turn_on("input_boolean.circadian")

    def condseq_on(self, switch=None, entity=None, brightness=None, t_fade=0, color=None, post_delay=0):
        """
            A function for conditional sequentilization
            Takes the following arguments:

            switch: An input boolean that's conditional for the sequence to
            keep running

            entity: The entity to be affected

            For lights:
            brightness: End brightness [0-255]
            fade: How long the fade should take (in seconds)
            color: End colour [X, Y]
            post_delay: How long after the action there should be an additional delay (in seconds)
        """
        device, entity_id = self.split_entity(self.light)
        if switch is not None:
            if self.get_state(switch) == "on":
                if device == "light":
                    if color is not None:
                        self.turn_on(entity, brightness = brightness, transition = t_fade * self.modifier, kelvin = color)
                        if self.get_state(switch) == "on":
                            time.sleep(t_fade * self.modifier)
                            time.sleep(post_delay * self.modifier)
                    else:
                        self.turn_on(entity, brightness = brightness, transition = t_fade * self.modifier)
                        if self.get_state(switch) == "on":
                            time.sleep(t_fade * self.modifier)
                            time.sleep(post_delay * self.modifier)
                self.turn_on(entity)

    """def test_blink(self, entity="", attribute="", old="", new="", kwargs=""):
        self.turn_on("light.monitor", kelvin=1000)

        for i in range(3):
            time.sleep(1)
            self.turn_on("light.monitor", flash = "short")
            self.turn_off("light.monitor")"""
