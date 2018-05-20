import appdaemon.plugins.hass.hassapi as hass
import sys
import subprocess

class RemoteMonitorManager(hass.Hass):

    def initialize(self, entity="", attribute="", old="", new="", kwargs=""):
        "Initializing"

        self.log("Initializing remote-monitor-manager")

        self.path = "/home/martin/scripts/remote-monitor-manager/script.sh"
        self.switch = "light.monitor"

        self.listen_state(self.run, self.switch, old="on", new="off")

    def run(self, entity="", attribute="", old="", new="", kwargs=""):
        "Function that'll run bash script"

        HOST="192.168.1.111"
        # Ports are handled in ~/.ssh/config since we use OpenSSH
        COMMAND="pmset displaysleepnow"

        ssh = subprocess.Popen(["ssh", "%s" % HOST, COMMAND],
                               shell=False,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
        result = ssh.stdout.readlines()
        if result == []:
            error = ssh.stderr.readlines()
            self.log(sys.stderr, "ERROR: %s" % error)
        else:
            self.log(result)
