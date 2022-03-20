from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from numpy import float64
import numpy.typing as npt


class ActuatorState(ABC):
    @abstractmethod
    def get_control_torque(self) -> npt.NDArray[float64]:
        pass


State = TypeVar("State", bound=ActuatorState)

class Actuator(ABC, Generic[State]):
    @property
    @abstractmethod
    def state(self) -> State:
        pass

    @state.setter
    @abstractmethod
    def state(self, state: State) -> None:
        pass

    @abstractmethod
    def actuate(self, control_torque: npt.NDArray[float64], dt: float, state: State) -> State:
        pass


