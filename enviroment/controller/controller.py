from abc import ABC, abstractmethod
from org.orekit.propagation import SpacecraftState


import typing


class Action:
    pass

class Controller(ABC):
    @abstractmethod
    def get_actions(self, state: SpacecraftState) -> typing.Sequence[Action]:
        pass



class SimpleController(Controller):
    pass


class RL_Controller(Controller):
    pass
