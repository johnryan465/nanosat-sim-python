from abc import ABC, abstractmethod
from typing import List

from nanosatsim.core.state.spacecraft import SpacecraftState


class Sensor(ABC):
    """
    This class defines a sensor for our satillite,
    these sensors will define a state provider,
    only sensor state providers are available to be
    used by the controllers.
    """

    @abstractmethod
    def get_new_state(self, state: SpacecraftState) -> List[float]:
        """
        This calculates the sensor values and sets the fields
        """

    @abstractmethod
    def get_name(self) -> str:
        """
        Return state provider names
        """
