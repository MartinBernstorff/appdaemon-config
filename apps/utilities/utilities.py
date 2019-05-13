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

class Utilities(hass.Hass):
    def initialize(self):
        self.log("Initializing {}".format(__name__))

    def setstate(self, lt, brightness=None, fade=None, color=None, switch=None):
        self.modulator = 1

        if switch != None:
            if self.get_state(switch) == "off":
                self.log("Switch turned off, exiting")
                return

        self.log("Set " + lt + " to fade to " + str(brightness) + " and color {}".format(str(color)) + "\n over " + str(fade * self.modulator) + "s")

        if brightness == None:
            brightness = g.c_brightness

        if color != None:
            self.turn_on(lt, brightness = brightness, transition = self.modulator * fade, xy_color = color)
        else:
            self.turn_on(lt, brightness = brightness, transition = self.modulator * fade)



        if brightness == 0:
            if fade != "":
                self.run_in(self.turn_off(lt), fade)
            else:
                self.turn_off(lt)
