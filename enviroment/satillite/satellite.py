from abc import ABC, abstractmethod
from typing import Iterable
from enviroment.controller.controller import Controller

from enviroment.utils.units import Weight
from org.orekit.propagation import SpacecraftState
from org.orekit.propagation import AdditionalStateProvider


"""
Satillite Base Class

The describes a satillite in a simulation.
- Mass
- Position
- Velocity
- Additional State


When we wish to have the satillite be able to influence its enviroment,
this will be done by having the satillite have some properties
(which can be controlled by the ACDS or be sensor values) which the physics 
engine can read and interprerate and give force values.


"""
class Satellite(ABC):
    @property
    @abstractmethod
    def mass(self) -> float:
        pass

    @mass.setter
    @abstractmethod
    def mass(self, mass: float) -> None:
        pass

    @property
    @abstractmethod
    def state(self) -> SpacecraftState:
        pass

    @state.setter
    @abstractmethod
    def state(self, state: SpacecraftState) -> None:
        pass

    @property
    @abstractmethod
    def controller(self) -> Controller:
        pass

    @controller.setter
    @abstractmethod
    def controller(self, controller: Controller) -> None:
        pass

    @abstractmethod
    def get_additional_state_providers(self) -> Iterable[AdditionalStateProvider]:
        pass
    
