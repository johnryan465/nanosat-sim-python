from abc import ABC, abstractmethod
from typing import List

import orekit
from org.orekit.propagation import \
    PythonAdditionalStateProvider  # type: ignore
from org.orekit.propagation import SpacecraftState


class Sensor(PythonAdditionalStateProvider):
    """
    This class defines a sensor for our satillite,
    these sensors will define a state provider,
    only sensor state providers are available to be
    used by the controllers.
    """

    def getAdditionalState(self, state: SpacecraftState) ->  List[float]:
        """
        Returns an Orekit State Provider which represents what the sensor records
        """
        return self.get_new_state(state)

    @abstractmethod
    def get_new_state(self, state: SpacecraftState) -> List[float]:
        """
        This calculates the sensor values and sets the fields
        """

    def getName(self) -> str:
        """
        Return state provider names
        """
        return self.get_name()

    @abstractmethod
    def get_name(self) -> str:
        """
        Return state provider names
        """
