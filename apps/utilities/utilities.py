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

        self.verbose = 1

    def scheduled_light_setter(self, kwargs):
        self.light_setter(**kwargs)

    def light_setter(self, lt, brightness=None, fade=None, xy_color=None, switch=None, kelvin=None, **kwargs):
        if self.verbose == 1:
            self.log("Parameters parsed:\n    lt: {}\n    brightness: {}\n    fade: {}\n    xy_color: {}\n    switch {}\n    kelvin: {}".format(lt, brightness, fade, xy_color, switch, kelvin))

        if switch != None:
            if self.get_state(switch) == "off":
                self.log("Switch turned off, exiting")
                return

        if brightness == None:
            brightness = g.c_brightness

        if brightness == 0:
            if fade != None:
                self.run_in(self.scheduled_turn_off, fade, entity_id=lt)
                self.log("Turning {} off after {}".format(lt, fade))
                if xy_color != None:
                    self.turn_on(lt, brightness = 1, transition = fade, xy_color = xy_color)
                elif kelvin != None:
                    self.turn_on(lt, transition = fade, kelvin = kelvin, brightness = 1)
                else:
                    self.turn_on(lt, brightness = 1, transition = fade)
            else:
                self.turn_off(lt)
                self.log("Turning {} off now".format(lt))
        elif brightness > 0:
            if xy_color != None:
                self.turn_on(lt, brightness = brightness, transition = fade, xy_color = xy_color)
            elif kelvin != None:
                self.turn_on(lt, transition = fade, kelvin = kelvin, brightness = brightness)
                self.log("Set " + lt + " to fade to " + str(brightness) + " and kelvin {}".format(str(kelvin)) + "\n over " + str(fade) + "s")
            else:
                self.turn_on(lt, brightness = brightness, transition = fade)



    def scheduled_turn_off(self, kwargs):
        self.turn_off(**kwargs)
