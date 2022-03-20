from abc import ABC, abstractmethod
from typing import List
from org.orekit.propagation import PythonAdditionalStateProvider  # type: ignore
from org.orekit.propagation import SpacecraftState


class Sensor(ABC, PythonAdditionalStateProvider):
    """
    This class defines a sensor for our satillite,
    these sensors will define a state provider,
    only sensor state providers are available to be
    used by the controllers.
    """

    def getAdditionalState(self, state: SpacecraftState) -> PythonAdditionalStateProvider:
        """
        Returns an Orekit State Provider which represents what the sensor records
        """
        return self.get_additional_state(state)

    def getName(self) -> str:
        return self.get_name()

    @abstractmethod
    def get_name(self) -> str:
        """
        Return state provider names
        """

    @abstractmethod
    def get_additional_state(self, state: SpacecraftState) -> List[float]:
        """
        This calculates the sensor values and sets the fields
        """
