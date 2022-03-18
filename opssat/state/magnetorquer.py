from typing import List
from org.orekit.propagation import PythonAdditionalStateProvider, AdditionalStateProvider  # type: ignore
from org.orekit.propagation import SpacecraftState

from spacecraft.sensorsat import SensorSatellite


class MagnetorquerStateProvider(PythonAdditionalStateProvider):
    def getName(self) -> str:
        return "dipole_moment"

    def getAdditionalState(self, state: SpacecraftState) -> List[float]:
        """
        This sets intended magnetic dipole
        """
        return [1.0, 1.0, 1.0]
