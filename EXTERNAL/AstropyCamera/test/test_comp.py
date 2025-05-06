import time

import numpy as np
import matplotlib.pyplot as plt

from Acspy.Clients.SimpleClient import PySimpleClient

cli = PySimpleClient()
cam = cli.getComponent("CAMERA")
mount = cli.getComponent("TELESCOPE_CONTROL")

mount.objfix(39.695396716044826, 125.83155601317783)
img_data = cam.getFrame("", "")

print(len(img_data))

mult = 5

width = int(1920 / mult)
height = int(1080 / mult)

img = np.frombuffer(img_data, dtype=np.uint8).reshape((height, width))

plt.figure(figsize=(8, 8))
plt.imshow(img, origin='lower')
plt.colorbar()
plt.show()
