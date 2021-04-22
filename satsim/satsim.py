import numpy as np
import threading
import astropy.coordinates import SkyCoord as sc

class Sat:
    def __init__(self):
        self.location = self.getLoc()
        self.attitude = sc(0,0, unit='deg', frame='icrs')
        self.saturation = 0
        self.battery = 10000
        self.system_modes = 
        {
                "opt_read": False
                "opt_cool": False
                "rad_mode": False
                "grv_mode": False
                "HGA_mode": "off"   #off/rx/tx
                "LGA_mode": "idle"  #idle/dup/tx
                "torquers": False
                "gyro_del": False
        }

    def inst_optical():
        """
        Main Telescope
        """
        pass

    def inst_radiation():
        """
        beta/gamma detector
        """
        pass

    def inst_gravitometer():
        """
        local gravity and potential gravity waves (rare)
        """
        pass

    def inst_hg_antenna():
        """
        tight beam antenna for high speed up/downlink
        has to point at your ground station.
        """
        pass

    def check_command_q():
        pass

    def update():
        pass

