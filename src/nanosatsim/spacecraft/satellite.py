from abc import ABC, abstractmethod

import numpy as np
from nanosatsim.spacecraft.controller import Controller
from numpy.typing import NDArray
from org.orekit.propagation import AdditionalStateProvider, SpacecraftState


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
        """
        Returns:
            state (SpacecraftState):  the state of the craft
        """

    @state.setter
    @abstractmethod
    def state(self, state: SpacecraftState) -> None:
        """
        Parameter:
            state (SpacecraftState):  the new state of the craft
        """

    @property
    @abstractmethod
    def controller(self) -> Controller:
        """
        Returns:
            controller (Controller):  the controller of the craft
        """

    @controller.setter
    @abstractmethod
    def controller(self, controller: Controller) -> None:
        """
        Parameter:
            controller (Controller):  sets the controller of the craft
        """

    @abstractmethod
    def get_inertia(self) -> NDArray[np.float64]:
        """
        Return the inertial tensor of the satillite
        """

    @abstractmethod
    def get_inertia_inverse(self) -> NDArray[np.float64]:
        """
        Returns the inverse inertial tensor
        """
