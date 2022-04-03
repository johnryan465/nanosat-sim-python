from typing import List
from nanosatsim.provider.spacecraft_state import AdditionalStateProvider, SpacecraftState


class ReactionWheelStateProvider(AdditionalStateProvider):
    def getName(self) -> str:
        return "reaction_wheel"

    def getAdditionalState(self, state: SpacecraftState) -> List[float]:
        """
        Sets the angular velocity of the reaction wheels
        """
        return [1.0, 1.0, 1.0]
