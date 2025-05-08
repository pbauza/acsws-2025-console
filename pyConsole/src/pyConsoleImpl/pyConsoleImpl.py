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
  
class pyConsoleImpl(CONSOLE_MODULE__POA.Console, ACSComponent, ContainerServices, ComponentLifecycle):
    def __init__(self):
        ACSComponent.__init__(self)
        ContainerServices.__init__(self)
        self._logger = self.getLogger()
    def printHello(self):
        print("Just printing 'Hello World!'")
        return "Hello World!"
    def setMode(self):
        pass
    def getMode(self):
        pass
    def cameraOn(self):
        pass
    def cameraOff(self):
        pass
    def moveTelescope(self):
        pass
    def getTelescopePosition(self):
        pass
    def getCameraImage(self):
        pass
    def setRGB(self):
        pass
    def setPixelBias(self):
        pass
    def setResetLevel(self):
        pass