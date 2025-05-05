# Python imports

# CORBA Stub Imports
import TELESCOPE_MODULE__POA

# ACS Imports
from Acspy.Servants.CharacteristicComponent import CharacteristicComponent
from Acspy.Servants.ContainerServices  import ContainerServices
from Acspy.Servants.ComponentLifecycle import ComponentLifecycle
from Acspy.Util.BaciHelper             import addProperty
from ACSImpl.DevIO                     import DevIO

# Local Package Imports
from stellarium.api import StellariumAPI

class StellariumDevIO(DevIO):
    """DevIO that returns a timestamp with its data."""
    def __init__(self, altazm):
        DevIO.__init__(self, 0.0)
        self.api = None
        if altazm == "alt":
            self.index = 0
        elif altazm == "azm":
            self.index = 1
        else:
            raise RuntimeException("Wrong DevIO type")

    def read(self):
        val = 0.0
        if self.api is not None:
            val = self.api.get_altaz()[self.index]
        return tuple((val,1191516502))

    def setApi(self, api):
        self.api = api
        

class StellariumComponent(TELESCOPE_MODULE__POA.TelescopeControl, CharacteristicComponent, ContainerServices, ComponentLifecycle):
    # Component class variables
    # Component class methods

    # Constructor
    def __init__(self):
        CharacteristicComponent.__init__(self)
        ContainerServices.__init__(self)
        self.api = None
        self.alt_devio = None
        self.azm_devio = None

    # Component Lifecycle
    def initialize(self):
        self.alt_devio = StellariumDevIO("alt")
        self.azm_devio = StellariumDevIO("azm")
        addProperty(self, "commandedAltitude")
        addProperty(self, "commandedAzimuth")
        addProperty(self, "actualAltitude", self.alt_devio)
        addProperty(self, "actualAzimuth", self.azm_devio)
        addProperty(self, "status")

    def execute(self):
        self.api = StellariumAPI()
        self.alt_devio.setApi(self.api)
        self.azm_devio.setApi(self.api)

    def cleanUp(self):
        self.api = None

    def aboutToAbort(self):
        self.api = None

    # Component Operations
    def objfix(self, altitude, azimuth):
        self.api.gradual_fov(60.0);
        self.setTo(altitude, azimuth);
        self.api.gradual_fov(5.0);

    def setTo(self, altitude, azimuth):
        # Commanded positions
        self._get_commandedAltitude().set_sync(altitude);
        self._get_commandedAzimuth().set_sync(azimuth);

        # Move telescope
        #self.api.move_to_altaz(altitude, azimuth);
        self.api.slew_to_altaz(altitude, azimuth);

    def offSet(self, altOffset, azOffset):
        # Calculate target position
        altitude = self._get_actualAltitude().get_sync()[0] + altOffset;
        azimuth = self._get_actualAzimuth().get_sync()[0] + azOffset;

        # Command Telescope
        self.setTo(altitude, azimuth)

    def zenith(self):
        # Calculate target position
        altitude = 90.0
        azimuth = self._get_actualAzimuth().get_sync()[0]

        # Command Telescope
        self.setTo(altitude, azimuth)

    def park(self):
        # Calculate target position
        altitude = 0.0
        azimuth = 0.0

        # Command Telescope
        self.setTo(altitude, azimuth)

    def setUncalibrated(self):
        self._get_status_().set_sync(0)

    def calibrateEncoders(self):
        self._get_status().set_sync(1)

    # Other methods
