# Client stubs and definitions, such as structs, enums, etc.
import CONSOLE_MODULE
# Skeleton infrastructure for server implementation
import CONSOLE_MODULE__POA
  
# Base component implementation
from Acspy.Servants.ACSComponent import ACSComponent
# Services provided by the container to the component
from Acspy.Servants.ContainerServices import ContainerServices
# Basic component lifecycle (initialize, execute, cleanUp and aboutToAbort methods)
from Acspy.Servants.ComponentLifecycle import ComponentLifecycle

from TYPES import Position, RGB, ImageType

from Acspy.Clients.SimpleClient import PySimpleClient

  
class pyConsoleImpl(CONSOLE_MODULE__POA.Console, ACSComponent, ContainerServices, ComponentLifecycle):
    def __init__(self):
        ACSComponent.__init__(self)
        ContainerServices.__init__(self)
        self._logger = self.getLogger()
        self.client = PySimpleClient()
        self.auto_schedule = False

        self.scheduler_client = self.client.getComponent("SCHEDULER")
        self.instrument_client = self.client.getComponent("INSTRUMENT")
        self.telescope_client = self.client.getComponent("TELESCOPE")

    def printHello(self):
        print("Just printing 'Hello World!'")
        return "Hello World!"

    def setMode(self, mode:bool):
        print("Starting method: setMode")
        if mode != self.auto_schedule:
            if mode:
                self.scheduler_client.start()
            else:
                self.scheduler_client.stop()
            self.auto_schedule = mode
                        
    def getMode(self):
        print("Starting method: getMode")
        if self.auto_schedule:
            return 'Automatic'
        else:
            return 'Manual'

    def cameraOn(self):
        print("Starting method: cameraOn")
        self.instrument_client.cameraOn()

    def cameraOff(self):
        print("Starting method: cameraOn")
        self.instrument_client.cameraOff()

    def getCameraImage(self, exposure_time:int):
        print("Starting method: getCameraImage")
        return self.instrument_client.takeImage(exposure_time)

    def setRGB(self, rgb:RGB):
        print("Starting method: setRGB")
        self.instrument_client.setRGB(rgb)

    def setPixelBias(self, bias:int):
        print("Starting method: setPixelBias")
        self.instrument_client.setPixelBias(bias)

    def setResetLevel(self, resetLevel:int):
        print("Starting method: setResetLevel")
        self.instrument_client.setResetLevel(resetLevel)
    
    def moveTelescope(self, position:Position):
        print("Starting method: moveTelescope")
        self.telescope_client.moveTo(position) # instead of moveTelescope

    def getTelescopePosition(self):
        print("Starting method: getTelescopePosition")
        self.telescope_client.getCurrentPosition() # instead of getTelescopePosition
