from nanosatsim.core.force.force_model import ForceModel
from nanosatsim.core.position.frame import Frame
from abc import ABC, abstractmethod
from typing import Iterable


class SpaceEnviroment(ABC):
    @abstractmethod
    def get_force_models(self) -> Iterable[ForceModel]:
        """
        Returns an iterable of force models which will apply forces to our satillite
        """

    @abstractmethod
    def get_base_frame(self) -> Frame:
        """
        Returns the base frame of our enviroment
        """
