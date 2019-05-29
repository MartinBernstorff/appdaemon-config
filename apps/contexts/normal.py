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

class Normal(hass.Hass):
    def initialize(self):
        self.log("Initializing {} with switch: {}".format(__name__, self.args["switch"]))

        self.listen_state(self.on, "input_select.context", new = "Normal")

        self.lights = ["light.gang",
                "light.loft_2",
                "light.reol_2",
                "light.monitor"
                  ]

        self.circadian_gen = self.get_app("circadian_gen")

        self.Utils = self.get_app("Utilities")

    def on(self, entity, attribute, old, new, kwargs):
        self.log("New context is Normal, turning on lights")
        self.circadian_gen.gen_c_brightness()
        self.circadian_gen.gen_c_colortemp()

        time.sleep(0.2)

        self.log("Proceeding to light adjustments")
        if old == "Cozy":
            self.log("Updating lights slowly from Cozy,\n    Color: {}\n    Brightness: {}".format(g.c_colortemp, g.c_brightness))

            for light in self.lights:
                self.Utils.light_setter(light, fade = 60)
                time.sleep(10)

            self.log("Finished light transition to Normal from Cozy")
        else:
            self.log("Updating lights quickly,\n    Color: {}\n    Brightness: {}".format(g.c_colortemp, g.c_brightness))

            for light in self.lights:
                self.Utils.light_setter(light, fade = 1)

            self.log("Finished transition to Normal")

        self.turn_on("input_boolean.circadian")
