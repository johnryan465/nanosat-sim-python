from abc import ABC, abstractmethod
from typing import Iterable

from org.orekit.propagation import SpacecraftState
from org.orekit.propagation import AdditionalStateProvider

from spacecraft.controller.controller import Controller



class Satellite(ABC):
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
    @property
    @abstractmethod
    def mass(self) -> float:
        """
        Returns:
            mass (float):  the current mass of the satillie
        """

    @mass.setter
    @abstractmethod
    def mass(self, mass: float) -> None:
        """
        Parameter:
            mass (float):  the new mass of the satillie
        """

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
