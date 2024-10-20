import time
import xpc
from telemetry import Telemetry

class WirelessXPTelemetry(Telemetry):
    def __init__(self, xpHost="localhost", xpPort=49009, port=0, timeout=100):
        self.xpc_client = xpc.XPlaneConnect(xpHost, xpPort, port, timeout)
    
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
        sim_params = {"Altitude AGL" : int(meters_to_feet * self.xpc_client.getDREF("sim/flightmodel/position/y_agl")[0]),
                      "IAS" : int(self.xpc_client.getDREF("sim/flightmodel/position/indicated_airspeed")[0])}
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
    
    def pauseSim(self, t):
        print(f"Pausing sim for {t} seconds.")
        self.xpc_client.pauseSim(True)
        time.sleep(2)

        # Toggle pause state to resume
        print("Resuming")
        self.xpc_client.pauseSim(False)

    def engineFire(self):
        self.xpc_client.sendDREF("sim/operation/failures/rel_engfir0", 6)

    def engineFail(self):
        self.xpc_client.sendDREF("sim/operation/failures/rel_engfai0", 6)


if __name__ == "__main__":
    data = WirelessXPTelemetry()
    data.monitor()
