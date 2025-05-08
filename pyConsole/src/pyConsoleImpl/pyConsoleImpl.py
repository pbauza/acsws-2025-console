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
    
    def getComponent(self, componentName:str):
        return self.client.getComponent(componentName)
    
    def getScheduler(self):
        return self.getComponent("SCHEDULER")

    def printHello(self):
        print("Just printing 'Hello World!'")
        return "Hello World!"

    def setMode(self, mode:bool):
        print("Starting method: setMode")
        scheduler = self.getScheduler()
        if mode != self.auto_schedule:
            if mode:
                scheduler.start()
            else:
                scheduler.stop()
            self.auto_schedule = mode
                        
    def getMode(self):
        print("Starting method: getMode")
        if self.auto_schedule:
            return 'Automatic'
        else:
            return 'Manual'

    def cameraOn(self):
        print("Starting method: cameraOn")
        #Code
        return "cameraOn method ended"

    def cameraOff(self):
        print("Starting method: cameraOff")
        #Code
        return "cameraOff method ended"

    def moveTelescope(self, position:Position):
        print("Starting method: moveTelescope")
        #Code
        return "moveTelescope method ended"

    def getTelescopePosition(self):
        print("Starting method: getTelescopePosition")
        #Code
        return "getTelescopePosition method ended"

    def getCameraImage(self):
        print("Starting method: getCameraImage")
        #Code
        return "getCameraImage method ended"

    def setRGB(self, rgb:RGB):
        print("Starting method: setRGB")
        #Code
        return "setRGB method ended"

    def setPixelBias(self, bias:int):
        print("Starting method: setPixelBias")
        #Code
        return "setPixelBias method ended"

    def setResetLevel(self, resetLevel:int):
        print("Starting method: setResetLevel")
        #Code
        return "ssetResetLevel method ended"

