from org.orekit.attitudes import AttitudeProviderModifier
from org.orekit.attitudes import AttitudeProvider
from org.orekit.attitudes import Attitude
from org.orekit.frames import Frame
from org.orekit.time import AbsoluteDate
from org.orekit.utils import PVCoordinatesProvider
from spacecraft.satellite import Satellite


class ControllerAttitude(AttitudeProviderModifier):
    """
    Update the variables which we will use to model the kinects which depend on
    the controller here.

    We can compose the Attitude Providers.
    """
    def __init__(self, base_provider: AttitudeProvider, satellite: Satellite) -> None:
        self.base_provider = base_provider
        self.satellite = satellite

    def getUnderlyingAttitudeProvider(self) -> AttitudeProvider:
        return self.base_provider

    def getAttitude(self, pvProv: PVCoordinatesProvider, date: AbsoluteDate, frame: Frame) -> Attitude:
        attitude = self.base_provider.getAttitude(pvProv, date, frame)
        # Todo: Input forces and accelerations based on reaction wheel and magentorquers
        return attitude
