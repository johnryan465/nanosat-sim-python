from abc import ABC, abstractmethod
import orekit
from org.orekit.propagation import SpacecraftState


import typing


class Action:
    """
    Action
    """


class Controller(ABC):
    """
    A base class for a controller for the satillite
    """
    @abstractmethod
    def get_actions(self, state: SpacecraftState) -> typing.Sequence[Action]:
        pass



class SimpleController(Controller):
    """
    A Basic Dummy controller
    """


class RLController(Controller):
    """
    A RL controller
    """
