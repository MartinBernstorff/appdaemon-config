import time
import datetime
import appdaemon.plugins.hass.hassapi as hass

#
# Carpediem app
#
# Args:
#   switch: The switch that initializes the script
#   factor: the input_select that determines the factor length

class CarpeDiem(hass.Hass):
    def initialize(self):
        self.log("Initializing carpe diem with switch: " + self.args["switch"])
        #Setup the switch object
        switch = self.args["switch"]

        #Reset switch to off
        self.reset()

        # Register callback
        self.on_handle = self.listen_state(self.carpe_diem, switch, new="on")

        #Reset the switch at 20:00 each day
        self.time = datetime.time(20, 0, 0)
        self.run_daily(self.reset, self.time)

        self.modulator = 2

    def carpe_diem(self, entity, attribute, old, new, kwargs):
        self.turn_off("input_boolean.circadian") #Turn off circadian temporarily
        self.turn_off("input_boolean.sunrise") #Turn off sunrise if it's stil on

        self.run_in(self.carpe_monitor, self.modulator * 1)
        self.run_in(self.carpe_bathroom, self.modulator * 1)

        self.run_in(self.carpe_worklight, self.modulator * 9)
        self.run_in(self.carpe_reol, self.modulator * 10)

        self.run_in(self.carpe_loft, self.modulator * 30)

        self.run_in(self.finished, self.modulator * 120)

    def carpe_monitor(self, kwargs):
        light = "light.monitor"
        self.setstate(light, self.global_vars["c_brightness"], 20, color=self.global_vars["c_colortemp"]) #Circadian hue

    def carpe_bathroom(self, kwargs):
        #Setup circadian dependencies
        #Make short bathroom light var
        light = "light.bathroom_2"
        if self.now_is_between("04:00:00", "12:00:00"):
            self.setstate(light, self.global_vars["c_brightness"], 5, self.global_vars["c_colortemp"]) #Circadian hue

    def carpe_reol(self, kwargs):
        #Make short reol light var
        light = "light.color_temperature_light_1"
        self.setstate(light, self.global_vars["c_brightness"], 40, self.global_vars["c_colortemp"]) #Circadian hue

    def carpe_loft(self, kwargs):
        #Make short reol light var
        light = "light.ikea_loft"
        self.setstate(light, self.global_vars["c_brightness"], 40, self.global_vars["c_colortemp"]) #Circadian hue

    def carpe_worklight(self, kwargs):
        #Make short reol light var
        light = "light.color_temperature_light_1_2"
        self.setstate(light, self.global_vars["c_brightness"], 30, self.global_vars["c_colortemp"]) #Circadian hue

    def carpe_hallway(self, kwargs):
        #Make short reol light var
        light = "light.hallway_2"
        if self.now_is_between("04:00:00", "12:00:00"):
            self.setstate(light, self.global_vars["c_brightness"], 30, self.global_vars["c_colortemp"]) #Circadian hue

    def setstate(self, lt, brightness, fade, color=""):
        switch = self.args["switch"]

        if self.get_state(switch) == "on":
            self.log("Set " + lt + " to fade in over " + str(fade * self.modulator) + "s")

            if self.get_state(switch) == "on":
                if color != "":
                    self.turn_on(lt, brightness=brightness, transition=self.modulator * fade, kelvin=color)
                else:
                    self.turn_on(lt, brightness=brightness, transition=self.modulator * fade)

            if self.get_state(switch) == "on":
                time.sleep(self.modulator * fade)
        else:
            self.log("Switch turned off, terminating")

    def reset(self, entity="", attribute="", old="", new="", kwargs=""):
        self.turn_off(self.args["switch"])

    def finished(self, entity="", attribute="", old="", new="", kwargs=""):
        self.turn_on("input_boolean.circadian") #Turn back on circadian
        self.set_state("input_select.context", state = "Normal")
        self.reset()
