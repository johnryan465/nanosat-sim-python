from abc import abstractmethod
import math
import numpy as np
import numpy.typing as npt
from numpy import float64
from nanosatsim.spacecraft.actuators import Actuator, ActuatorState


class SetOfMagnetorquersState(ActuatorState):
    def __init__(self, torque: npt.NDArray[float64], magnetic_diopole: npt.NDArray[float64]) -> None:
        self.torque = torque
        self.magnetic_diopole = magnetic_diopole

    def get_magnetic_dipole(self) -> npt.NDArray[np.float64]:
        return self.magnetic_diopole

    def get_control_torque(self) -> npt.NDArray[float64]:
        return self.torque


class SetOfMagnetorquers(Actuator[SetOfMagnetorquersState]):
    def __init__(self) -> None:
        self._state = SetOfMagnetorquersState(np.zeros(3), np.zeros(3))
        self.max_magnetic_dipole = 30.0
        self.mean_magnetic_field = 0.948

    @property
    def state(self) -> SetOfMagnetorquersState:
        return self._state

    @state.setter
    def state(self, state: SetOfMagnetorquersState) -> None:
        self._state = state

    def actuate(self, magneticField_body: npt.NDArray[float64], t_mtr: npt.NDArray[float64]) -> SetOfMagnetorquersState:

        # computing the magneticDipole with cross-product-control-law
        magneticDipole_body_Am2 = np.cross(magneticField_body, t_mtr) * (-1 / math.pow(self.mean_magnetic_field, 2))

        # unit conversion to Tesla
        magneticField_body_T = magneticField_body * (1E-9)

        # check saturation in each magnetorquer
        for i in range(0,3):
            if (abs(magneticDipole_body_Am2[i]) > self.max_magnetic_dipole):
                magneticDipole_body_Am2[i] = np.sign(magneticDipole_body_Am2[i]) * self.max_magnetic_dipole

        # computing the torque
        torque_body = np.cross(magneticDipole_body_Am2, magneticField_body_T)
        self.state = SetOfMagnetorquersState(torque_body, magneticDipole_body_Am2)
        return self.state
