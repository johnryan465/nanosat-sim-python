from typing import List
from org.orekit.propagation import PythonAdditionalStateProvider, AdditionalStateProvider  # type: ignore
from org.orekit.propagation import SpacecraftState


class MagnetometerStateProvider(PythonAdditionalStateProvider):
    def getName(self) -> str:
        return "dipole_moment"

    def getAdditionalState(self, state: SpacecraftState) -> List[float]:
        """
        This sets the magnetic dipole moment
        """
        return [0.0, 0.0, 0.0] # [1.0, 1.0, 1.0]
