import numpy as np
from gamma import gamma_sensor
from heartbeat import heartbeat_module
from location import location_module
from time import sleep
from astropy.coordinates import SkyCoord as sc
from os import system

#debugg to rebuild the file every test
system('cp command_q test_q')

ONSAT_FILESTORE = "DATA"
DOWNLINK_FILESTORE = "../store/data"

class sat:
    def __init__(self):
        self.attitude = sc(0,0, unit='deg', frame='icrs')
        self.battery = 100.00
        self.maneuver_TTC = 0 #time to completion
        self.gyro_saturation = 0
        self.modules = {
            "heartbeat"      : heartbeat_module(), 
            "location"       : location_module(),
            #"power"         : power_manager(), 
            #"attitude"      : attitude_module(), 
            "gamma_sensor"   : gamma_sensor()
        }

    def check_command_q(self):
        cur_batch = []
        with open("command_q","r") as q:
            com_q = q.read().splitlines()
            for com in com_q:
                if int(com.split(":")[0]) == self.modules["heartbeat"].mod_get("MTE")[0]:
                    cur_batch.append(com)
        return cur_batch


    def spin(self):       
        while True:
            MTE = self.modules["heartbeat"].mod_get("MTE")[0]
            print(MTE)
            batch = self.check_command_q()

            for c in batch:
                print(c)
                com = c.split(":")
                if com[1] == "GET" and len(com) == 4:
                    res = self.modules[com[2]].mod_get(com[3])
                elif com[1] == "SET" and len(com) == 5:
                    res = self.modules[com[2]].mod_set(com[3],com[4])
                elif com[1] == "EXE" and len(com) == 5:
                    res = self.modules[com[2]].mod_exe(com[3],com[3])
                else:
                    res = (-1, "BAD COMMAND: " + c)
                print(res)
            
            for m in self.modules:
                self.modules[m].mod_update()
            if self.modules["heartbeat"].mod_get("kill")[0] == 1:
                print("heading to bed")
                return

            with open("status", "r+") as statfile:
                statfile.seek(0)
                statfile.truncate()
                statfile.write(str(MTE))

            sleep(1)


if __name__ == "__main__":
    BoSLOO = sat()
    BoSLOO.spin()

