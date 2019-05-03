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

    def on(self, entity, attribute, old, new, kwargs):
        self.log("New context is Normal, turning on lights")

        self.turn_on("input_boolean.circadian")

        self.log("Updating lights quickly,\n    Color: {}\n    Brightness: {}".format(g.c_colortemp, g.c_brightness))

        lights = ["light.loft_2",
                  "light.reol_2",
                  "light.monitor"
                  ]

        for light in lights:
            self.turn_on(light,
                         transition = 1,
                         kelvin = g.c_colortemp,
                         brightness = g.c_brightness)
            time.sleep(0.2)

        self.turn_off("input_boolean.circadian")
        time.sleep(1)
        self.turn_on("input_boolean.circadian")
        self.log("Finished transitioning to normal")
