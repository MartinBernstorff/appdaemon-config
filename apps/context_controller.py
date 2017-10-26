import appdaemon.appapi as appapi
import time
import datetime

"""
 Off_scheduler

 Args:
   switch: The switch that's required for the script to run
   entity: The entity to be controlled
"""

class ContextController(appapi.AppDaemon):

    def initialize(self, entity="", attribute="", old="", new="", kwargs=""):
        # For single button
        self.listen_event(self.movie_mode, "click", entity_id = "binary_sensor.switch_158d0001a1f52f", click_type = "long_click_press")

    def movie_mode(self, entity, attribute, old, new="", kwargs=""):
        self.log("{} turned {}".format(entity, new))
        if self.get_state("input_select.context") != "Movie-mode":
            self.set_state("input_select.context", state="Movie-mode")
        else:
            self.set_state("input_select.context", state="Normal")
