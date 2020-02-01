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

class CarpeMieke(hass.Hass):
    def initialize(self):
        self.log("Initializing {} with switch: {}".format(__name__, self.args["switch"]))

        self.listen_state(self.on_from_boolean, "input_boolean.carpemieke", new = "on")

        self.Utils = self.get_app("Utilities")

        self.modulator = 1

    def on(self):
        self.log("Starting carpe Mieke")

        self.turn_off("input_boolean.circadian") #Turn off circadian temporarily
        self.turn_off("input_boolean.sunrise") #Turn off sunrise if it's stil on

        g.c_colortemp = 2000
        g.c_brightness = 200
        g.persistent_hallway_light = True

    def reset(self, entity="", attribute="", old="", new="", kwargs=""):
        self.turn_off("input_boolean.carpemieke")

    def on_from_boolean(self, entity, attribute, old, new, kwargs):
        self.log("Starting from boolean")
        self.on()
        time.sleep(1)

        """ A list of lists containing:
        Entity id, delay, fade duration
        """

        lights = [
            ["light.monitor", 2, 30],
            ["light.bathroom_2", 2, 20],
            ["light.reol_3", 2, 240],
            ["light.loft_3", 210, 300],
            ["light.gang_2", 60, 300],
        ]

        duration = 0  * self.modulator

        for light in lights:
            time.sleep(1)
            self.run_in(self.Utils.scheduled_light_setter,
                        light[1] * self.modulator,
                        lt=light[0],
                        fade=light[2],
                        switch="input_boolean.carpemieke",
                        kelvin=g.c_colortemp)

            if light[1] + light[2] > duration:
                duration = light[1] + light[2]

        self.set_state("input_select.context", state = "Carpe Mieke")

        time.sleep(duration + 5)
        self.reset()
        self.log("Finished carpe mieke!")
