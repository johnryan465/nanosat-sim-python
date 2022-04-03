from typing import List
from org.orekit.propagation import PythonAdditionalStateProvider  # type: ignore
from nanosatsim.core.actuator import Actuator
from nanosatsim.core.state.spacecraft import SpacecraftState


class OrekitActuator(PythonAdditionalStateProvider):
    def __init__(self, actuator: Actuator) -> None:
        super().__init__()
        self.actuator = actuator

    def getAdditionalState(self, state: SpacecraftState) -> List[float]:
        """
        Returns an Orekit State Provider which represents what the sensor records
        """
        return self.actuator.get_new_state(state)

    def getName(self) -> str:
        """
        Return state provider names
        """
        return self.actuator.get_name()
