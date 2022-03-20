from abc import ABC, abstractmethod
from nanosatsim.spacecraft.actions import ActuatorAction
import orekit
from org.orekit.propagation import SpacecraftState


from typing import Iterable


class Controller(ABC):
    """
    A base class for a controller for the satillite
    """
    @abstractmethod
    def get_actions(self, state: SpacecraftState) -> Iterable[ActuatorAction]:
        pass



class SimpleController(Controller):
    """
    A Basic Dummy controller
    """
    def get_actions(self, state: SpacecraftState) -> Iterable[ActuatorAction]:
        return []


class RLController(Controller):
    """
    A RL controller
    """
