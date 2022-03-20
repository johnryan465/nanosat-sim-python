
from dataclasses import dataclass
import math
from nanosatsim.spacecraft.actions import ActuatorAction
from nanosatsim.spacecraft.actuators import Actuator, ActuatorState
from numpy.typing import NDArray
import numpy as np


class SetOfReactionWheelsState(ActuatorState):
    def __init__(self, angular_velocity: NDArray[np.float64]) -> None:
        self._angular_velocity = angular_velocity

    def get_angular_velocity(self) -> NDArray[np.float64]:
        return self._angular_velocity

@dataclass
class ReactionWheelAction(ActuatorAction):
    goal_angular_velocity: NDArray[np.float64]


class SetOfReactionWheels(Actuator[SetOfReactionWheelsState, ReactionWheelAction]):
    def __init__(self, state: SetOfReactionWheelsState) -> None:
        self._state = state

    @property
    def state(self) -> SetOfReactionWheelsState:
        return self._state

    @state.setter
    def state(self, state: ActuatorState) -> None:
        if not isinstance(state, SetOfReactionWheelsState):
            raise Exception("Wrong State")
        self._state = state

    def actuate(self, action: ReactionWheelAction) -> None:
        pass
