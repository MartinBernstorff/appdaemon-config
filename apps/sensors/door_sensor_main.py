import appdaemon.plugins.hass.hassapi as hass

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

class DoorSensorMain(hass.Hass):

    def initialize(self):

        self.handle = None

        # Check some Params

        self.global_vars["door_opened_recently"] = 0

        # Subscribe to sensors
        if "sensor" in self.args:
            self.listen_state(self.opened, self.args["sensor"], new = "on")
        else:
            self.log("No sensor specified, doing nothing")

    def opened(self, entity, attribute, old, new, kwargs):
        if self.global_vars["door_opened_recently"] == 0:
            self.global_vars["door_opened_recently"] = 1

            self.context = self.get_state("input_select.context")

            if self.context == "Away":
                self.log("Door sensor turning on with context {}".format(self.context))
                self.set_state("input_select.context", state = "Normal")
                self.turn_on("light.hallway", transition = 0.5, xy_color = self.global_vars["c_colortemp"], brightness = 0.6 * self.global_vars["c_brightness"])
        else:
            self.log("Door was opened recently, not firing script again.")

        delay = 60
        self.cancel_timer(self.handle)
        self.handle = self.run_in(self.delay_end, delay)

    def delay_end(self, kwargs):
        self.log("Timer ended, setting door_opened_recently to 0")
        self.global_vars["door_opened_recently"] = 0

    def cancel(self):
        self.cancel_timer(self.handle)
