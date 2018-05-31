import appdaemon.plugins.hass.hassapi as hass
import circadiangen
import time
import datetime

#
# Carpediem app
#
# Args:
#   switch: The switch that initializes the script
#   factor: the input_select that determines the factor length

class MovieMode(hass.Hass):
    def initialize(self):
        self.log("Initializing {} with switch: {}".format(__name__, self.args["switch"]))

        #Setup the switch object
        switch = self.args["switch"]

        self.listen_state(self.on, "input_select.context", new = "Movie-mode")
        self.listen_state(self.off, "input_select.context", old = "Movie-mode")

        #Register callback for switch turning on
        self.listen_state(self.playing, "input_select.playing_state", new = "playing", old = "paused")
        self.listen_state(self.paused, "input_select.playing_state", new = "paused", old = "playing")

        #Update input_select if state changes independent of button_single
        self.listen_state(self.set_playing_state_playing, "media_player.rasplex", new="playing", old = "paused")
        self.listen_state(self.set_playing_state_paused, "media_player.rasplex", new="paused", old = "playing")

    def on(self, entity, attribute, old, new, kwargs):
        self.log("Moviemode on!")
        self.turn_off("input_boolean.circadian") #Turn off circadian temporarily
        if self.get_state("media_player.pioneer") == "off":
            self.turn_on("media_player.pioneer")
            i = 0
            while (i < 15) and self.get_state("media_player.pioneer") == "off":
                time.sleep(1)
                i += 1
                self.log("Receiver is off, checking in 1 second, i = {}".format(i))
        elif self.get_state("media_player.pioneer") == "on":
            self.log("Receiver is already on, proceding")

        # Turn on the lights
        self.setstate("light.monitor", 50, 10)
        self.setstate("light.ikea_loft", 0, 8)
        self.setstate("ight.color_temperature_light_1", 1, 13)

        # Switch source to tuner, to power on speakers
        if self.get_state("media_player.pioneer", "source") != "TUNER":
            i = 0
            while (i < 10) and self.get_state("media_player.pioneer", "source") != "TUNER":
                self.call_service("media_player/select_source", entity_id = "media_player.pioneer", source = "TUNER")
                i += 1
                time.sleep(1)
                self.log("Source is not TUNER, trying again")
        else:
            self.log("Source is already tuner")

        self.call_service("media_player/volume_set", entity_id = "media_player.pioneer", volume_level = 0.8)
        time.sleep(2)
        self.call_service("media_player/select_source", entity_id = "media_player.pioneer", source = "RPI")

        if self.get_state("media_player.pioneer", "source") != "RPI" and self.get_state("media_player.pioneer", "source") == "TUNER":
            i = 0
            while (i < 10) and self.get_state("media_player.pioneer", "source") != "RPI":
                self.call_service("media_player/select_source", entity_id = "media_player.pioneer", source = "RPI")
                i += 1
                time.sleep(1)
        else:
            self.log("Source is already RPI")
        self.call_service("media_player/volume_set", entity_id = "media_player.pioneer", volume_level = 0.7)

        self.turn_off("light.ikea_loft")
        self.turn_off("light.hallway")

    def off(self, entity, attribute, old, new, kwargs):
        # Quick fades if rasplex is already stopped
        if self.get_state("media_player.rasplex") != "playing":
            self.log("Rasplex not playing, initializing quick fade")
            self.turn_off("media_player.pioneer")
            self.turn_on("input_boolean.circadian") #Turn circadian adjustments back on
            self.log("Moviemode off!")
            self.call_service("media_player/media_stop", entity_id = "media_player.rasplex")
        else: # Slower fade, if switch is turned off during credits
            self.log("Rasplex playing, slow fade")
            self.setstate("light.monitor", self.global_vars["c_brightness"], 80, self.global_vars["c_colortemp"])
            self.setstate("ight.color_temperature_light_1", self.global_vars["c_brightness"], 80, self.global_vars["c_colortemp"])
            self.setstate("light.ikea_loft", self.global_vars["c_brightness"], 80, self.global_vars["c_colortemp"])

            vollevel = self.get_state("media_player.pioneer", "volume_level")

            i = 0
            while (i<10):
                vollevel -= (0.005 * i)
                self.call_service("media_player/volume_set", entity_id = "media_player.pioneer", volume_level = vollevel)
                time.sleep(4)
                i += 1

            self.turn_off("media_player.pioneer")
            self.turn_on("input_boolean.circadian") #Turn circadian adjustments back on
            self.log("Moviemode off!")
            self.call_service("media_player/media_stop", entity_id = "media_player.rasplex")

    def playing(self, entity, attribute, old, new, kwargs):
        if self.get_state("input_select.context") == "Movie-mode":
            self.log("Activating playing actions {}".format(self.time()))
            self.turn_off("group.all_lights")

    def paused(self, entity, attribute, old, new, kwargs):
        self.log("Activating paused actions at {}".format(self.time()))

        if self.get_state("input_select.context") == "Movie-mode":
            self.setstate("light.monitor", 100, 10, self.global_vars["c_colortemp"])
            self.setstate("ight.color_temperature_light_1", 1, 10, self.global_vars["c_colortemp"])

    def setstate(self, lt, bness, fade, color=""):
        self.modulator = 1

        self.log("Set " + lt + " to fade in " + str(fade * self.modulator) + "s")

        if color != "":
            self.turn_on(lt, brightness = bness, transition = self.modulator * fade, xy_color = color)
        else:
            self.turn_on(lt, brightness = bness, transition = self.modulator * fade)

    def set_playing_state_playing(self, entity, attribute, old, new, kwargs):
        self.set_state("input_select.playing_state", state = "playing")

    def set_playing_state_paused(self, entity, attribute, old, new, kwargs):
        self.set_state("input_select.playing_state", state = "paused")
