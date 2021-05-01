import numpy as np
import threading
from astropy.coordinates import SkyCoord as sc
from os import system

#debugg to rebuild the file every test
system('cp command_q test_q')


class Sat:
    def __init__(self):
        self.location = self.get_loc()
        self.attitude = sc(0,0, unit='deg', frame='icrs')
        self.battery = 10000
        self.MTE = 0
        self.kill = False
        self.system_modes = {
                "opt_read": False,
                "opt_cool": False,
                "rad_mode": False,
                "grv_mode": False,
                "HGA_mode": "off",   #off/rx/tx
                "LGA_mode": "idle",  #idle/dup/tx, for power these modes will be automatic
                "torquers": False,
                "gyro_del": False,
        }
        self.maneuver_q = []
        self.maneuver_TTC = 0 #time to completion
        self.gyro_saturation = 0

        self.lens_temp =

    def get_loc(self):
        """
        retrieve location from orbit sim
        """
        pass

    def get_status(self, command="null"):
        print("BoSLOO STATUS:")
        print("Feelin Fine <3")

    def inst_optical(self, command="null"):
        """
        Main Telescope
        """
        pass

    def inst_ultraviolet(self, command="null"):
        """
        UV band Telescope
        """
        pass
    
    def inst_hydrogen_line(self, command="null"):
        """
        hydrogen line radio telescope
        """


    def inst_radiation(self, command="null"):
        """
        beta/gamma detector
        """
        pass

    def inst_gravitometer(self, command="null"):
        """
        local gravity and potential gravity waves (rare)
        """
        pass

    def inst_hg_antenna(self, command="null"):
        """
        tight beam antenna for high speed up/downlink
        has to point at your ground station.
        """
        pass

    def check_command_q(self):
        with open('test_q', 'r+') as q:
            commands = q.read().splitlines()
            remainder = ""
            for com in commands:
                if int(com.split(":")[0]) == self.MTE:
                    print("got com -> ", com)

                    com_type = com.split(":")[1]
                    if com_type.strip() == "status":
                        self.get_status(com)
                    elif com_type.strip() == "point":
                        self.set_target(com)
                    elif com_type.strip() == "uload":
                        self.upload(com)
                    elif com_type.strip() == "dload":
                        self.download()
                    elif com_type.strip() == "list":
                        self.list_drive()
                    elif com_type.strip() == "status":
                    elif com_type.strip() == "status":
                    elif com_type.strip() == "status":
                    elif com_type.strip() == "status":
                    elif com_type.strip() == "status":
                    elif com_type.strip() == "status":
                    elif com_type.strip() == "status":
                    elif com_type.strip() == "status":
                    elif com_type.strip() == "status":
                    elif com_type.strip() == "status":

                else:
                    remainder += com + '\n'
            q.truncate(0)
            q.seek(0)
            q.write(remainder)

    def update(self):
        self.check_command_q()
        if not self.kill:
            threading.Timer(1, self.update).start()
        else:
            print("heading to bed")
        self.MTE += 1


if __name__ == "__main__":
    BoSLOO = Sat()
    BoSLOO.update()
    #while True:
    #    try:
    #        pass
    #    except KeyboardInterrupt:
    #        BoSLOO.kill = True
    #        print("Good night!")
    #        break

