from abc import ABC, abstractmethod
import orekit
from org.orekit.propagation import SpacecraftState


from typing import Iterable


class Action:
    """
    Action
    """


class Controller(ABC):
    """
    A base class for a controller for the satillite
    """
    @abstractmethod
    def get_actions(self, state: SpacecraftState) -> Iterable[Action]:
        pass



class SimpleController(Controller):
    """
    A Basic Dummy controller
    """
    def get_actions(self, state: SpacecraftState) -> Iterable[Action]:
        return []


class RLController(Controller):
    """
    A RL controller
    """
