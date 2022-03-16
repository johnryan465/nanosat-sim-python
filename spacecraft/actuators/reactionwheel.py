
import imp
import math
from spacecraft.actuators.actuators import Actuator, ActuatorState
import numpy.typing as npt
import numpy as np
from numpy import float64, floating
from abc import abstractmethod


class SetOfReactionWheelsState(ActuatorState):
    def __init__(self, control_torque: npt.NDArray[np.float64], angular_velocity: npt.NDArray[np.float64], inertia: float) -> None:
        self.control_torque = control_torque
        self.angular_velocity = angular_velocity
        self.inertia = inertia

    def get_angular_momentum_norm(self, x: npt.NDArray[np.float64]) -> floating:
        return np.linalg.norm(self.get_angular_momentum(x))

    def get_angular_momentum(self, x: npt.NDArray[np.float64]) -> npt.NDArray[np.float64]:
        # h_{w,n} = I_{n,s}a_n^T\omega + I_{n,s}\omega_n
        return (self.angular_velocity + x) * self.inertia

    def get_angular_velocity(self) -> npt.NDArray[np.float64]:
        return self.angular_velocity

    def get_control_torque(self) -> npt.NDArray[float64]:
        return self.control_torque


class SetOfReactionWheels(Actuator[SetOfReactionWheelsState]):
    def __init__(self, state: SetOfReactionWheelsState) -> None:
        self._state = state
        self.max_torque = 1
        self.max_angular_velocity = 1
        self.intertia = 1
        self.max_angular_accel_approx = 1

    @property
    def state(self) -> SetOfReactionWheelsState:
        return self._state

    @state.setter
    def state(self, state: ActuatorState) -> None:
        if not isinstance(state, SetOfReactionWheelsState):
            raise Exception("Wrong State")
        self._state = state

    def actuate(self, control_torque: npt.NDArray[float64], dt: float, state: SetOfReactionWheelsState) -> SetOfReactionWheelsState:
        # check limits of torques
        for i in range(0, 2):
            if abs(control_torque[i]) > self.max_torque:
                control_torque[i] = np.sign(control_torque[i]) * self.max_torque

        # computing angular acceleration
        α = control_torque * (1 / self.intertia)

        # computing desired angular velocity
        current_ω = self.state.get_angular_velocity()

        goal_ω = current_ω + (α * dt)

        # check saturation in the angular velocity,and change the
        # torque accordingly
        for i in range(0, 3):
            if abs(goal_ω[i]) > self.max_angular_velocity:
                control_torque[i] = np.sign(
                    control_torque[i]) * (self.max_angular_velocity - abs(current_ω[i])) * self.intertia / dt
                goal_ω[i] = self.max_angular_velocity * np.sign(goal_ω)

        if abs(np.linalg.norm(current_ω)) - abs(np.linalg.norm(goal_ω)) > (math.sqrt(4 * self.max_angular_accel_approx* self.max_angular_accel_approx) * dt):
            raise Exception("Error in the processing of angular velocity")

        # updating instantaneous torque and the angular velocity
        self._state = SetOfReactionWheelsState(control_torque, goal_ω, self.intertia)
        return self._state
