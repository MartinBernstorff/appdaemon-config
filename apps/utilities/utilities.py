import appdaemon.plugins.hass.hassapi as hass
import circadiangen
import time
import datetime
import globals as g
import random

#
# Carpediem app
#
# Args:
#   switch: The switch that initializes the script
#   factor: the input_select that determines the factor length

class Utilities(hass.Hass):
    def initialize(self):
        self.log("Initializing {}".format(__name__))

        self.verbose = 0

        self.ikea_lights = ["light.arbejds_2",
                    "light.reol_3",
                    "light.loft_3",
                    "light.gang_2"]

    def scheduled_light_setter(self, kwargs):
        self.light_setter(**kwargs)

    def light_setter(self, lt, brightness=None, fade=None, xy_color=None, switch=None, kelvin=None, **kwargs):
        time.sleep(random.uniform(0, 0.2))
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
                if self.get_state(lt) == "off":
                    return
                self.run_in(self.scheduled_turn_off, fade+1, entity_id=lt)
                self.log("Turning {} off after {}".format(lt, fade))
                if xy_color != None:
                    self.turn_on(lt, transition = fade, xy_color = xy_color, brightness = 1)
                elif kelvin != None:
                    self.turn_on(lt, transition = fade, kelvin = kelvin, brightness = 1)
                else:
                    self.turn_on(lt, transition = fade, brightness = 1)
            else:
                self.turn_off(lt)
                self.log("Turning {} off now".format(lt))
        elif brightness > 0:
            if xy_color != None:
                self.turn_on(lt, transition = fade, xy_color = xy_color, brightness = brightness)
            elif kelvin != None:
                if lt in self.ikea_lights: # Since IKEA-lights no longer accept values outside of min/max mireds, set specifics
                    if kelvin > 5000:
                        kelvin = 5000
                    elif kelvin < 1000:
                        kelvin = 1000

                    mireds = 250+(1-(kelvin-1000)/4000)*(454-250)
                    self.turn_on(lt, transition = fade, brightness = brightness, color_temp = mireds)
                    if self.verbose == 1:
                        self.log("Setting {} as ikea_light with mireds {}".format(lt, mireds))
                else:
                    self.turn_on(lt, transition = fade, brightness = brightness, kelvin = kelvin)
            else:
                self.turn_on(lt, transition = fade, brightness = brightness, kelvin = g.c_colortemp)

    def scheduled_turn_off(self, kwargs):
        time.sleep(random.uniform(0, 0.2))
        self.turn_off(kwargs["entity_id"])
        time.sleep(random.uniform(0, 0.2))

        if self.get_state(kwargs["entity_id"]) == "off":
            self.log("{} turned off on schedule".format(kwargs["entity_id"]))
        else:
            self.log("ERROR: {} not turned off".format(kwargs["entity_id"]))
