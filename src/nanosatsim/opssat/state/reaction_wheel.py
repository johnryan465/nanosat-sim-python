from typing import List
from org.orekit.propagation import PythonAdditionalStateProvider, AdditionalStateProvider  # type: ignore
from org.orekit.propagation import SpacecraftState


class ReactionWheelStateProvider(PythonAdditionalStateProvider):
    def getName(self) -> str:
        return "reaction_wheel"

    def getAdditionalState(self, state: SpacecraftState) -> List[float]:
        """
        Sets the angular velocity of the reaction wheels
        """
        return [1.0, 1.0, 1.0]