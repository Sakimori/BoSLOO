import numpy as np
from sensor_module import gamma_sensor
from time import sleep
from astropy.coordinates import SkyCoord as sc
from os import system

#debugg to rebuild the file every test
system('cp command_q test_q')

ONSAT_FILESTORE = "DATA"
DOWNLINK_FILESTORE = "../store/data"

class sat:
    def __init__(self):
        self.location = self.get_loc()
        self.attitude = sc(0,0, unit='deg', frame='icrs')
        self.battery = 100.00
        self.MTE = 0
        self.kill = False
        self.maneuver_q = []
        self.maneuver_TTC = 0 #time to completion
        self.gyro_saturation = 0
        self.modules = [gamma_sensor(),gamma_sensor()]

    def get_loc(self):
        """
        retrieve location from orbit sim
        """
        return (10,10,10)

    def get_status(self, command="null"):
        status_string = ""

    def check_command_q(self):
        cur_batch = []
        with open("test_q","r") as q:
            com_q = q.read().splitlines()
            for com in com_q:
                if int(com.split(":")[0]) == self.MTE:
                    cur_batch.append(com)
        return cur_batch


    def spin(self):       
        while True:
            for m in self.modules:
                m.mod_update()
                print(m.mod_get("detections"))
                if self.MTE % 10 == 0:
                    m.mod_set("flush", 1)
            batch = self.check_command_q()
            print("MTE:", self.MTE)
            print("COMS:", batch)
            if self.MTE == 5:
                self.kill = False
            if self.kill:
                print("heading to bed")
                return
            self.MTE += 1
            sleep(1)


if __name__ == "__main__":
    BoSLOO = sat()
    BoSLOO.spin()

