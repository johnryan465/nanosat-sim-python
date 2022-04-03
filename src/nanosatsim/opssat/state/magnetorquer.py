from typing import List
from nanosatsim.provider.spacecraft_state import AdditionalStateProvider, SpacecraftState

from nanosatsim.spacecraft.sensorsat import SensorSatellite


class MagnetorquerStateProvider(AdditionalStateProvider):
    def getName(self) -> str:
        return "dipole_moment"

    def getAdditionalState(self, state: SpacecraftState) -> List[float]:
        """
        This sets intended magnetic dipole
        """
        return [1.0, 1.0, 1.0]
