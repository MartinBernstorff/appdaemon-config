import appdaemon.plugins.hass.hassapi as hass
import datetime
import time
import globals as g

#
# Circadian app
#
# Args:
#   None atm.

class CircadianGen(hass.Hass):

    def initialize(self):
        self.log("CircadianGen initialized")
        self.now = self.datetime()
        b = self.now + datetime.timedelta(seconds=3)

        self.utils = self.get_app("Utilities")

        self.update_offset()
        self.gen_c_brightness()
        self.gen_c_colortemp()

        #Setup the input_selects
        self.listen_state(self.update_offset, "input_select.circadian_hour")
        self.listen_state(self.update_offset, "input_select.circadian_minute")

        self.listen_state(self.gen_c_colortemp, "input_boolean.circadian")
        self.listen_state(self.gen_c_colortemp, "input_select.circadian_hour")
        self.listen_state(self.gen_c_colortemp, "input_select.circadian_minute")

        self.listen_state(self.gen_c_brightness, "input_boolean.circadian")
        self.listen_state(self.gen_c_brightness, "input_select.circadian_hour")
        self.listen_state(self.gen_c_brightness, "input_select.circadian_minute")

        #Setup run_every
        self.run_every(self.gen_c_brightness, b, 20)
        self.run_every(self.gen_c_colortemp, b, 20)

    def gen_c_brightness(self, entity="", attribute="", old="", new="", kwargs=""):
        self.now = self.datetime()
        t0 = self.now.replace(hour=5, minute=0, second=0) + g.c_offset
        t1 = self.now.replace(hour=6, minute=0, second=0) + g.c_offset
        t2 = self.now.replace(hour=13, minute=0, second=0) + g.c_offset
        t3 = self.now.replace(hour=19, minute=0, second=0) + g.c_offset
        t4 = self.now.replace(hour=21, minute=0, second=0) + g.c_offset
        t5 = self.now.replace(hour=21, minute=15, second=0) + g.c_offset

        if self.now > t0 and self.now <= t1:
            self.set_c_brightness(2.65, 0, t1, t0)
        elif self.now > t1 and self.now <= t2:
            self.set_c_brightness(2.5, 2.65, t2, t1)
        elif self.now > t2 and self.now <= t3:
            self.set_c_brightness(2.5, 2.65, t3, t2)
        elif self.now > t3 and self.now <= t4:
            self.set_c_brightness(0.5, 2.5, t4, t3)
        elif self.now > t4 and self.now <= t5:
            self.set_c_brightness(0.08, 0.5, t5, t4)
        else:
            g.c_offsetbrightness = 20

        # self.log("Set new circ brightness {} at {}".format(g.c_brightness, self.now))

    def set_c_brightness(self, endbness, startbness, endtime, starttime):
        base = 255
        start = startbness
        end = endbness
        fadelength = (endtime-starttime).seconds
        position = (self.now-starttime).seconds

        g.c_brightness = (start + (end - start) * position / fadelength) * base

    def gen_c_colortemp(self, entity="", attribute="", old="", new="", kwargs=""):
        self.now = self.datetime()
        t0 = self.now.replace(hour=0, minute=0, second=0) + g.c_offset
        t1 = self.now.replace(hour=6, minute=1, second=0) + g.c_offset
        t2 = self.now.replace(hour=10, minute=0, second=0) + g.c_offset
        t3 = self.now.replace(hour=19, minute=0, second=0) + g.c_offset
        t4 = self.now.replace(hour=20, minute=45, second=0) + g.c_offset
        t5 = self.now.replace(hour=21, minute=15, second=0) + g.c_offset

        if self.now > t0 and self.now <= t1:
            self.set_c_colortemp(1000, 1000, t0, t1)
        elif self.now > t1 and self.now <= t2:
            self.set_c_colortemp(2000, 4000, t1, t2)
        elif self.now > t2 and self.now <= t3:
            self.set_c_colortemp(4000, 4000, t2, t3)
        elif self.now > t3 and self.now <= t4:
            self.set_c_colortemp(4000, 2500, t3, t4)
        elif self.now > t4 and self.now <= t5:
            self.set_c_colortemp(2500, 1000, t4, t5)
        else:
            g.c_colortemp = 1000

    def set_c_colortemp(self, starttemp, endtemp, starttime, endtime):
        fadelength = (endtime-starttime).seconds
        position = (self.now-starttime).seconds

        self.colortemp = starttemp + (endtemp - starttemp) * position / fadelength

        g.c_colortemp = self.colortemp

        #self.log("Set new colortemp {} at {}".format(g.c_colortemp, self.time()))

    def update_offset(self, entity="", attribute="", old="", new="", kwargs=""):
        self.hour = int(self.get_state("input_select.circadian_hour"))
        self.minute = int(self.get_state("input_select.circadian_minute"))
        g.c_offset = datetime.timedelta(hours=self.hour, minutes=self.minute)
        self.log("circadiangen_updated time offset set to {}".format(g.c_offset))

"""
[ 0.674, 0.322 ] #Red initial
[ 0.5268, 0.4133 ] #Warm orange
[ 0.4255, 0.3998 ] #Bright orange
"""
