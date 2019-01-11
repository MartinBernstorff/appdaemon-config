import appdaemon.plugins.hass.hassapi as hass
import globals as g

#
# App to turn lights on when motion detected then off again after a delay
#
# Use with constrints to activate only for the hours of darkness
#
# Args:
#
# sensor: binary sensor to use as trigger
# entity_on : entity to turn on when detecting motion, can be a light, script, scene or anything else that can be turned on
# entity_off : entity to turn off when detecting motion, can be a light, script or anything else that can be turned off. Can also be a scene which will be turned on
# delay: amount of time after turning on to turn off again. If not specified defaults to 60 seconds.
#
# Release Notes
#
# Version 1.1:
#   Add ability for other apps to cancel the timer
#
# Version 1.0:
#   Initial Version

class MotionSensor(hass.Hass):

    def initialize(self):

        self.handle = None

        # Check some Params

        # Subscribe to sensors
        if "sensor" in self.args:
            self.listen_state(self.motion, self.args["sensor"])
        else:
            self.log("No sensor specified, doing nothing")

    def motion(self, entity, attribute, old, new, kwargs):
        if new == "on":
            self.context = self.get_state("input_select.context")
            self.log("Motion sensor activated with context {}".format(self.context))
            if self.context == "Normal":
                self.turn_on("light.hallway_2", transition = 0.5, kelvin = g.c_colortemp - 300, brightness = 0.6 * g.c_brightness)

            elif self.context == "Cozy":
                self.turn_on("light.hallway_2", transition = 1, kelvin = 2000, brightness = 80)

            elif self.context == "Movie-mode":
                if self.get_state("input_select.playing_state") == "paused":
                    self.turn_on("light.hallway_2", kelvin = g.c_colortemp, transition = 0.5, brightness = 150)
                    self.turn_on("light.bathroom_2", transition = 0.5, kelvin = g.c_colortemp, brightness = g.c_brightness)
                elif self.get_state("input_select.playing_state") == "playing":
                    self.turn_on("light.hallway_2", transition = 0.5, kelvin = g.c_colortemp, brightness = 1)

            delay = 300
            self.cancel_timer(self.handle)
            self.handle = self.run_in(self.light_off, delay)

    def light_off(self, kwargs):
        if self.get_state("light.bathroom_2") == "on":
            self.cancel_timer(self.handle)
            self.handle = self.run_in(self.light_off, 120)
        elif g.persistent_hallway_light == True:
            self.cancel_timer(self.handle)
            print("Persistent hallway light: {}".format(g.persistent_hallway_light))
        else:
            self.turn_off("light.hallway_2")

    def cancel(self):
        self.cancel_timer(self.handle)
