from abc import ABC, abstractmethod
from typing import Generic, Iterable, TypeVar
from nanosatsim.core.actuator import Actuator
from nanosatsim.core.sensor import Sensor

from nanosatsim.core.state.spacecraft import SpacecraftState as _SpacecraftState
from nanosatsim.core.vector import Vector as _Vector
from nanosatsim.core.controller.controller import Controller as _Controller


SpacecraftState = TypeVar("SpacecraftState", bound=_SpacecraftState)
Controller = TypeVar("Controller", bound=_Controller)
Vector = TypeVar("Vector", bound=_Vector)


class Satellite(Generic[SpacecraftState, Controller, Vector], ABC):
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
    def get_inertia(self) -> Vector:
        """
        Returns:
            inertia (Vector):  the inertia of the craft
        """

    @abstractmethod
    def get_inertia_inverse(self) -> Vector:
        """
        Returns:
            inertia_inverse (Vector):  the inverse of the inertia of the craft
        """

    @abstractmethod
    def get_sensors(self) -> Iterable[Sensor]:
        """
        This returns a list of sensors which the satillite has
        """

    @abstractmethod
    def get_actuators(self) -> Iterable[Actuator]:
        """
        This returns a list of actuators
        """
