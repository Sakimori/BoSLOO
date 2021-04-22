import numpy as np
import threading
from astropy.coordinates import SkyCoord as sc

class Sat:
    def __init__(self):
        self.location = self.getLoc()
        self.attitude = sc(0,0, unit='deg', frame='icrs')
        self.saturation = 0
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

    def getLoc(self):
        pass

    def inst_optical(self):
        """
        Main Telescope
        """
        pass

    def inst_ultraviolet(self):
        """
        UV band Telescope
        """
        pass
    
    def inst_Hydrogen_line(self):
        """
        hydrogen line radio telescope
        """


    def inst_radiation(self):
        """
        beta/gamma detector
        """
        pass

    def inst_gravitometer(self):
        """
        local gravity and potential gravity waves (rare)
        """
        pass

    def inst_hg_antenna(self):
        """
        tight beam antenna for high speed up/downlink
        has to point at your ground station.
        """
        pass

    def check_command_q(self):
        with open('test_q', 'r+') as q:
            commands = q.readlines()
            remainder = ""
            for com in commands:
                if int(com.split(":")[0]) == self.MTE:
                    print("got com -> ", com)
                else:
                    remainder += com
            q.truncate(0)
            q.seek(0)
            q.write(remainder)

    def update(self):
        self.check_command_q()
        self.MTE += 1
        if not self.kill:
            threading.Timer(1, self.update).start()
        else:
            print("heading to bed")


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

