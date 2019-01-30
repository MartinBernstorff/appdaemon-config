import appdaemon.plugins.hass.hassapi as hass
import datetime
import globals as g

#
# Circadian app
#
# Args:
#   None atm

class CircadianSetter(hass.Hass):
    # List of lights with entity_id, brightness coefficient
    lights = [["light.monitor", 1.8],
              ["light.bathroom_2", 1.4],
              ["light.reol_2", 0.4],
              ["light.loft_2", 0.6],
              ["light.gang", 1]]

    def initialize(self):
        #Get current time and small time delta to initiate run_every
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
                self.setlight(light[0], 120, light[1])
            # self.log("Updating lights, time is {}, color temp is {} and brightness is {}".format(self.now.time(), g.c_colortemp, g.c_brightness))
        else:
            self.log("Circadian switch is off, lights not updated")

    def set_lights_quick(self, entity="", attribute="", old="", new="", kwargs=""):
        if self.get_state("input_boolean.circadian") == "on" and self.get_state("input_select.context") == "Normal":
            self.log("Updating lights quickly,\n    Kelvin: {}\n    Brightness: {}".format(g.c_colortemp, g.c_brightness))
            for light in self.lights:
                self.setlight(light[0], 3, light[1])
        else:
            # self.log("Circadian switch is off, lights not updated")
            pass

    def setlight(self, light, transition, modifier):
        if self.get_state(light) == "on":
            self.log("Adjusting {}".format(light))
            if (light == "light.loft_2") or (light == "light.reol_2"):
                self.turn_on(light,
                             transition = transition,
                             kelvin = (g.c_colortemp - 400),
                             brightness = modifier * g.c_brightness)
            elif light == "light.monitor":
                self.turn_on(light,
                             transition = transition,
                             kelvin = g.c_colortemp - 400,
                             brightness = modifier * (g.c_brightness) + 60)
            else:
                self.turn_on(light,
                             transition = transition,
                             kelvin = g.c_colortemp,
                             brightness = modifier * g.c_brightness)
