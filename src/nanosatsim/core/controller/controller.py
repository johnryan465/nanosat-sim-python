from abc import ABC, abstractmethod
from nanosatsim.core.controller.actions import Action
from nanosatsim.core.state.spacecraft import SpacecraftState


from typing import Iterable


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
