import sys
import os
sys.path.append(os.path.dirname(__file__))  # Add the current directory to the path
import xpc
from telemetry import Telemetry

class LocalXPTelemetry(Telemetry):
    def __init__(self):
        self.xpc = xpc.XPlaneConnect()
    
    def getData(self):
        """
        Latitude (deg)
        Longitude (deg)
        Altitude (m above MSL)
        Pitch (deg)
        Roll (deg)
        True Heading (deg)
        Gear (0=up, 1=down)
        """
        meters_to_feet = 3.28084
        sim_params = {"Altitude AGL" : meters_to_feet * self.xpc.getDREF("sim/flightmodel/position/y_agl")[0],
                      "IAS" : self.xpc.getDREF("sim/flightmodel/position/indicated_airspeed")[0]}
        #posi = self.xpc.getPOSI()
        # sim_params = {
        #               "Latitude": posi[0],
        #               "Longitude": posi[1],
        #               "Altitude": posi[2] * meters_to_feet,
        #               "Pitch": posi[3],
        #               "Roll": posi[4],
        #               "True Heading": posi[5],
        #               }
        return sim_params
