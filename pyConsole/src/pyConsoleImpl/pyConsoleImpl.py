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

from SYSTEMErrImpl import (
    AlreadyInAutomaticExImpl, 
    SystemInAutoModeExImpl, 
    CameraIsOffExImpl,
    PositionOutOfLimitsExImpl)
  
class pyConsoleImpl(CONSOLE_MODULE__POA.Console, ACSComponent, ContainerServices, ComponentLifecycle):
    def __init__(self):
        ACSComponent.__init__(self)
        ContainerServices.__init__(self)
        self._logger = self.getLogger()
        self.client = PySimpleClient()
        self.auto_schedule = False
        self.is_camera_on = False

        self.scheduler_client = self.client.getComponent("SCHEDULER")
        self.instrument_client = self.client.getComponent("INSTRUMENT")
        self.telescope_client = self.client.getComponent("TELESCOPE")
    
    def info(self, msg:str):
        self._logger.info(msg)
    def debug(self, msg:str):
        self._logger.debug(msg)
    def error(self, msg:str):
        self._logger.error(msg)
    def warning(self, msg:str):
        self._logger.warning(msg)
    def critical(self, msg:str):
        self._logger.critical(msg)

    def printHello(self):
        self.info("Just printing 'Hello World!'")
        return "Hello World!"

    def setMode(self, mode:bool):
        self.debug("Starting method: setMode")
        if mode != self.auto_schedule:
            if mode:
                self.scheduler_client.start()
            else:
                self.scheduler_client.stop()
        if mode and self.auto_schedule:
            raise AlreadyInAutomaticExImpl
        self.auto_schedule = mode
                        
    def getMode(self):
        self.debug("Starting method: getMode")
        if self.auto_schedule:
            return 'Automatic'
        else:
            return 'Manual'

    def cameraOn(self):
        self.debug("Starting method: cameraOn")
        if self.auto_schedule:
            raise SystemInAutoModeExImpl
        self.is_camera_on = True
        self.instrument_client.cameraOn()

    def cameraOff(self):
        self.debug("Starting method: cameraOn")
        if self.auto_schedule:
            raise SystemInAutoModeExImpl
        self.is_camera_on = False
        self.instrument_client.cameraOff()

    def getCameraImage(self, exposure_time:int):
        self.debug("Starting method: getCameraImage")
        if self.auto_schedule:
            raise SystemInAutoModeExImpl
        if not self.is_camera_on:
            raise CameraIsOffExImpl
        return self.instrument_client.takeImage(exposure_time)

    def setRGB(self, rgb:RGB):
        self.debug("Starting method: setRGB")
        if not self.is_camera_on:
            raise CameraIsOffExImpl
        self.instrument_client.setRGB(rgb)

    def setPixelBias(self, bias:int):
        self.debug("Starting method: setPixelBias")
        if not self.is_camera_on:
            raise CameraIsOffExImpl
        self.instrument_client.setPixelBias(bias)

    def setResetLevel(self, resetLevel:int):
        self.debug("Starting method: setResetLevel")
        if not self.is_camera_on:
            raise CameraIsOffExImpl
        self.instrument_client.setResetLevel(resetLevel)
    
    def moveTelescope(self, position:Position):
        self.debug("Starting method: moveTelescope")
        if self.auto_schedule:
            raise SystemInAutoModeExImpl
        if position.az < 0 or position.az > 360 or position.el < 0 or position.el > 90:
            raise PositionOutOfLimitsExImpl
        self.telescope_client.moveTo(position) # instead of moveTelescope

    def getTelescopePosition(self):
        self.debug("Starting method: getTelescopePosition")
        return self.telescope_client.getCurrentPosition() # instead of getTelescopePosition
