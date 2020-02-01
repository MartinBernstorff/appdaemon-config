import appdaemon.plugins.hass.hassapi as hass
import datetime
import globals as g
import time as time

#
# Circadian app
#
# Args:
#   None atm

class CircadianSetter(hass.Hass):
    # List of lights with entity_id, brightness coefficient
    lights = [["light.monitor", 1.8],
              ["light.bathroom_2", 1.4],
              ["light.reol_3", 0.8],
              ["light.loft_3", 0.6],
              ["light.gang_2", 1],
              ["light.arbejds_2", 0.38]]

    def initialize(self):
        #Get current time and small time delta to initiate run_every
        self.utils = self.get_app("Utilities")

        self.now = self.datetime()
        b = self.now + datetime.timedelta(0, 120)

        self.log("{} initiated".format(__name__))

        #Run every 4 minutes
        self.run_every(self.set_lights, b, 240)

        #Run when circadian switch is turned on
        self.listen_state(self.set_lights_quick, "input_boolean.circadian", new = "on")

        #Run when offset is changed
        self.listen_state(self.set_lights_quick, "input_select.circadian_hour")
        self.listen_state(self.set_lights_quick, "input_select.circadian_minute")

        self.set_lights_quick()

    def set_lights(self, entity="", attribute="", old="", new="", kwargs=""):
        if self.get_state("input_boolean.circadian") == "on" and self.get_state("input_select.context") == "Normal":
            for light in self.lights:
                if light[0] == "light.monitor":
                    self.utils.light_setter(lt=light[0], fade=120, brightness=g.c_brightness*light[1]+20, kelvin=g.c_colortemp)
                else:
                    self.utils.light_setter(lt=light[0], fade=120, brightness=g.c_brightness*light[1], kelvin=g.c_colortemp)
            # self.log("Updating lights, time is {}, color temp is {} and brightness is {}".format(self.now.time(), g.c_colortemp, g.c_brightness))
        else:
            self.log("Circadian switch is off, lights not updated")

    def set_lights_quick(self, entity="", attribute="", old="", new="", kwargs=""):
        if self.get_state("input_boolean.circadian") == "on" and self.get_state("input_select.context") == "Normal":
            self.log("Updating lights quickly,\n    Kelvin: {}\n    Brightness: {}".format(g.c_colortemp, g.c_brightness))
            for light in self.lights:
                if light[0] == "light.monitor":
                    self.utils.light_setter(lt=light[0], fade=120, brightness=g.c_brightness*light[1]+20, kelvin=g.c_colortemp)
                else:
                    self.utils.light_setter(lt=light[0], fade=3, brightness=g.c_brightness*light[1], kelvin=g.c_colortemp)
                time.sleep(0.5)
        else:
            # self.log("Circadian switch is off, lights not updated")
            pass
