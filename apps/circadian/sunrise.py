import appdaemon.plugins.hass.hassapi as hass
import time
import datetime
from rgb_xy import Converter

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

        self.entity = "light.bathroom_2" # The light to act as sun

        self.listen_state(self.rise_instant, self.args["switch"], new="on") # Callback for testing

        self.listen_state(self.set_alarm, "input_select.sunrise_hour") # Callback for testing
        self.listen_state(self.set_alarm, "input_select.sunrise_minute") # Callback for testing
        self.listen_state(self.set_alarm, "input_boolean.sunrise_alarm") # Callback for testing

    def set_alarm(self, entity="", attribute="", old="", new="", kwargs=""):
        self.alarm = None
        if self.get_state("input_boolean.sunrise_alarm") == "on":
            self.hour = self.get_state("input_select.sunrise_hour") # hour here
            self.minute = self.get_state("input_select.sunrise_minute")# minute her
            self.alarm_time = self.parse_time("{}:{}:00".format(self.hour, self.minute))

            self.log("Setting alarm to {}:{}".format(self.hour, self.minute))
            self.alarm = self.run_daily(self.rise_instant, self.alarm_time)

    def rise_instant(self, entity="", attribute="", old="", new="", kwargs=""):
        self.natural()

    def rise_delay(self, entity="", attribute="", old="", new="", kwargs=""):
        self.modifier = 1
        self.delay = 75 # Time in minutes to wait for sunrise, 45 + smart period (30) for Sleep as Android default
        self.turn_off("input_boolean.circadian")
        self.log("The sun is rising in {} mins!".format(self.modifier * self.delay))
        self.sunrise_timer = self.run_in(self.natural, self.modifier * self.delay*60)

    #######################
    # Different sequences #
    #######################

    def red_only(self):
        self.condseq_on(switch=self.switch, entity=self.entity, brightness=1, t_fade=1, color=[0.674, 0.322])
        self.condseq_on(switch=self.switch, entity=self.entity, brightness=10, t_fade=1800, color=[0.674, 0.322])
        self.condseq_on(switch=self.switch, entity=self.entity, brightness=100, t_fade=1800, color=[0.5268, 0.4133])
        self.turn_on("input_boolean.circadian")

    def natural(self, *args, **kwargs):
        self.log("Natural sunrise is running with switch {switch}, light {light} and modifier {modifier}".format(switch=self.switch, light=self.entity, modifier = self.modifier))
        # self.condseq_on(switch=self.switch, entity=self.entity, brightness=1, t_fade=1, color=conv.rgb_to_xy(255, 0, 0))
        self.condseq_on(switch=self.switch, entity="light.monitor", brightness=1, t_fade=1, color=3000)
        self.condseq_on(switch=self.switch, entity="light.monitor", brightness=1, t_fade=500, color=3000)
        self.condseq_on(switch=self.switch, entity="light.monitor", brightness=15, t_fade=400, color=3000)
        self.condseq_on(switch=self.switch, entity=self.entity, brightness=1, t_fade=1, color=3000)
        self.condseq_on(switch=self.switch, entity=self.entity, brightness=1, t_fade=899, color=3000)
        self.condseq_on(switch=self.switch, entity=self.entity, brightness=255, t_fade=900, color=3000)
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
        device, entity_id = self.split_entity(self.entity)
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
