from dataclasses import dataclass
from typing import List
import numpy as np
from numpy.typing import NDArray
from numpy import float64
from nanosatsim.core.state.spacecraft import SpacecraftState
from nanosatsim.core.controller.actions import Action
from nanosatsim.core.actuator import Actuator, ActuatorState


class SetOfMagnetorquersState(ActuatorState):
    def __init__(self, magnetic_diopole: NDArray[float64]) -> None:
        self.magnetic_diopole = magnetic_diopole

    def get_magnetic_dipole(self) -> NDArray[np.float64]:
        return self.magnetic_diopole


@dataclass
class MagnetorquersAction(Action):
    goal_magnetic_dipole: NDArray[np.float64]


class SetOfMagnetorquers(Actuator[SetOfMagnetorquersState, MagnetorquersAction]):
    def __init__(self, state: SetOfMagnetorquersState) -> None:
        self._state = state

    @property
    def state(self) -> SetOfMagnetorquersState:
        return self._state

    @state.setter
    def state(self, state: SetOfMagnetorquersState) -> None:
        self._state = state

    def actuate(self, action: MagnetorquersAction) -> None:
        pass

    def get_name(self) -> str:
        return "set_of_magnetorquers"

    def get_new_state(self, state: SpacecraftState) -> List[float]:
        return []
