import time

from Acspy.Clients.SimpleClient import PySimpleClient

cli = PySimpleClient()
m = cli.getComponent("TELESCOPE_CONTROL")

time.sleep(2)
#m.park()
m.objfix(45.0, 45.0)
time.sleep(2)

#print(m.status)
#print(m.status.get_sync()[0])
#m.calibrateEncoders()
#print(m.status.get_sync()[0])
#print(m.actualAltitude.get_sync()[0])
#print(m.actualAzimuth.get_sync()[0])
#m.zenith()
#print(m.actualAltitude.get_sync()[0])
#print(m.actualAzimuth.get_sync()[0])
