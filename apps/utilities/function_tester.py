import appdaemon.plugins.hass.hassapi as hass

# Function tester – uses initialize to test functions

class FunctionTester(hass.Hass):
    def initialize(self):
        self.log("Initializing {}".format(__name__))

        self.turn_on("light.ikea_loft", transition = "1", kelvin = "2000", brightness = "200")
