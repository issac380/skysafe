import time
import random
from XP.XPConnect.telemetry_xp_local import LocalXPTelemetry
from XP.XPConnect.telemetry_xp_wireless import WirelessXPTelemetry

#client = LocalXPTelemetry()
client = WirelessXPTelemetry("10.0.0.203", 49009, 0, 1000) #CHOOSE THIS IF WIRELESS

altitudes = []
speeds = []

time_to_fail = random.randint(10, 60)
time_to_fail = 10
time.sleep(time_to_fail)
client.engineFail()

while True:
    data = client.getData()
    print(f"Altitude (AGL): {data['Altitude AGL']}, Indicated Airspeed: {data['IAS']}")
    altitudes.append(data['Altitude AGL'])
    speeds.append(data['IAS'])
    if data['Altitude AGL'] < 10:
        break
    time.sleep(1)

print(altitudes)
print(speeds)