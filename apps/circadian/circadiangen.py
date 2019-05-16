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
        self.run_every(self.gen_c_brightness, b, 63)
        self.run_every(self.gen_c_colortemp, b, 65)

    def gen_c_brightness(self, entity="", attribute="", old="", new="", kwargs=""):
        self.now = self.datetime()

        times = [
            ["00:00:00", 0],
            ["04:00:00", 0],
            ["05:00:00", 2.5],
            ["12:00:00", 2.65],
            ["18:00:00", 2.5],
            ["20:00:00", 1.3],
            ["20:30:00", 0.5],
            ["21:15:00", 0.08],
            ["23:59:59", 0]
        ]

        self.previous_time_str = None
        self.previous_datetime = None
        self.previous_brightness = None

        self.i = 0

        for time in times:
            current_date_str = str(self.now.day) + "/" + str(self.now.month) + "/" + str(self.now.year)
            current_datetime = datetime.datetime.strptime(current_date_str + " " + time[0],
                                                 "%d/%m/%Y %H:%M:%S") + g.c_offset
            current_brightness = time[1]

            if self.i == 0:
                self.log("First time, continuing")

            elif self.now > self.previous_datetime and self.now <= current_datetime:
                self.log("Brightness time is between {} and {}".format(self.previous_datetime, current_datetime))
                self.set_c_brightness(current_brightness, self.previous_brightness,
                                      current_datetime, self.previous_datetime)
            else:
                pass

            self.previous_time_str = time[0]
            self.previous_datetime = current_datetime
            self.previous_brightness = time[1]
            self.i += 1

    def set_c_brightness(self, endbness, startbness, endtime, starttime):
        base = 255
        start = startbness
        end = endbness
        fadelength = (endtime-starttime).seconds
        position = (self.now-starttime).seconds

        g.c_brightness = (start + (end - start) * position / fadelength) * base
        self.log("g.c_brightness: {}".format(g.c_brightness))

        # self.log("\nstartbness: {}\nendbness: {}\nFadelength: {}\nPosition: {}\ng.c_brightness: {}".format(startbness, endbness, fadelength, position, g.c_brightness))

    def gen_c_colortemp(self, entity="", attribute="", old="", new="", kwargs=""):
        self.now = self.datetime()

        times = [
            ["00:00:00", 1000],
            ["05:01:00", 2000],
            ["09:00:00", 5250],
            ["16:30:00", 5250],
            ["18:00:00", 4500],
            ["20:00:00", 3000],
            ["20:30:00", 1000],
            ["23:59:59", 1000]
        ]

        self.previous_colortemp_time_str = None
        self.previous_colortemp_datetime = None
        self.previous_colortemp = None

        self.i = 0

        for time in times:
            current_date_str = str(self.now.day) + "/" + str(self.now.month) + "/" + str(self.now.year)
            current_datetime = datetime.datetime.strptime(current_date_str + " " + time[0],
                                                 "%d/%m/%Y %H:%M:%S") + g.c_offset
            current_colortemp = time[1]

            if self.i == 0:
                self.log("First time, continuing")

            elif self.now > self.previous_colortemp_datetime and self.now <= current_datetime:
                self.log("Colortemp time is between {} and {}".format(self.previous_colortemp_datetime, current_datetime))
                self.set_c_colortemp(current_colortemp, self.previous_colortemp,
                                      current_datetime, self.previous_colortemp_datetime)
            else:
                pass

            self.previous_colortemp_time_str = time[0]
            self.previous_colortemp_datetime = current_datetime
            self.previous_colortemp = time[1]
            self.i += 1

    def set_c_colortemp(self, endtemp, starttemp, endtime, starttime):

        fadelength = (endtime-starttime).seconds
        position = (self.now-starttime).seconds

        self.colortemp = starttemp + (endtemp - starttemp) * position / fadelength

        g.c_colortemp = self.colortemp

        self.log("g.c_colortemp: {}".format(g.c_colortemp))

        # self.log("\nStarttemp: {}\nEndtemp: {}\nFadelength: {}\nPosition: {}\ng.c_colortemp: {}".format(starttemp, endtemp, fadelength, position, g.c_colortemp))

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
