# Python imports

# CORBA Stub Imports
import CAMERA_MODULE__POA

# ACS Imports
from Acspy.Servants.CharacteristicComponent import CharacteristicComponent
from Acspy.Servants.ContainerServices  import ContainerServices
from Acspy.Servants.ComponentLifecycle import ComponentLifecycle
from Acspy.Util.BaciHelper             import addProperty
from ACSImpl.DevIO                     import DevIO

# Local Package Imports
from astrocam.api import AstrocamAPI

class AstrocamDevIO(DevIO):
    """DevIO that returns a timestamp with its data."""
    def __init__(self, altazm):
        DevIO.__init__(self, 0.0)
        self.api = None
        self.val = 0.0

    def read(self):
        return tuple((self.val,1191516502))

    def write(self, val):
        self.val = val

    def setApi(self, api):
        self.api = api
        

class AstrocamComponent(CAMERA_MODULE__POA.Camera, CharacteristicComponent, ContainerServices, ComponentLifecycle):
    # Component class variables
    # Component class methods

    # Constructor
    def __init__(self):
        CharacteristicComponent.__init__(self)
        ContainerServices.__init__(self)
        self.api = None
        self.shtspeed_devio = None
        self.isospeed_devio = None

    # Component Lifecycle
    def initialize(self):
        self.shtspeed_devio = AstrocamDevIO("sht")
        self.isospeed_devio = AstrocamDevIO("iso")
        addProperty(self, "shutterSpeed", self.shtspeed_devio)
        addProperty(self, "isoSpeed", self.isospeed_devio)
        self.mount = self.getComponent("TELESCOPE_CONTROL")

    def execute(self):
        self.api = AstrocamAPI()
        self.shtspeed_devio.setApi(self.api)
        self.isospeed_devio.setApi(self.api)

    def cleanUp(self):
        self.api = None
        self.releaseComponent(self.mount.name)
        self.mount = None

    def aboutToAbort(self):
        self.api = None
        self.mount = None

    # Component Operations
    def getFrame(self, exposureTime, iso):
        alt = self.mount.actualAltitude.get_sync()[0]
        azm = self.mount.actualAzimuth.get_sync()[0]
        return self.api.retrieve_raw_image(alt, azm)
    
    def on(self):
        pass

    def off(self):
        pass

    # Other methods
