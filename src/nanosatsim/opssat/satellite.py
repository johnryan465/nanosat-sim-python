from typing import Iterable
from nanosatsim.opssat.state import OPSSATState
import orekit
import numpy as np
from numpy.typing import NDArray
from numpy import array
from nanosatsim.opssat.actuators.magnetorquer import SetOfMagnetorquers, SetOfMagnetorquersState
from nanosatsim.opssat.actuators.reactionwheel import SetOfReactionWheels, SetOfReactionWheelsState

from nanosatsim.core.state.spacecraft import SpacecraftState
from nanosatsim.core.actuator import Actuator
from nanosatsim.core.controller.controller import Controller, SimpleController
from nanosatsim.core.sensor import Sensor


from nanosatsim.core.satellite import Satellite
from nanosatsim.opssat.sensors.magnetometer import Magnetometer


class OPSSAT(Satellite):
    """
    This defines the OPSSAT Mission Satillite

    Mass: 5.777673 kg

    Deployed COG = [39.93895,-37.19563,-166.4495] mm

    Deployed MOI = [
        65.77296 0.002580676 -0.2336325
        0.002580676 56.47602 0.05447529
        -0.2336325 0.05447529 16.50073
    ]  (
        10³ kg ∙ mm2
        10³ kg ∙ mm2
        10³ kg ∙ mm2
    )
    """

    def __init__(self) -> None:

        self._state = OPSSATState(5.777673)
        self._magnetometer = Magnetometer()
        self._controller = SimpleController()
        self._reaction_wheels = SetOfReactionWheels(SetOfReactionWheelsState(np.zeros(3)))
        self._magnetorquer = SetOfMagnetorquers(SetOfMagnetorquersState(np.zeros(3)))

    def get_inertia(self) -> NDArray[np.float64]:
        return array([
            [65.77296, 0.002580676, -0.2336325],
            [0.002580676, 56.47602, 0.05447529],
            [-0.2336325, 0.05447529, 16.50073]
        ])

    def get_inertia_inverse(self) -> NDArray[np.float64]:
        return np.linalg.inv(self.get_inertia())

    @ property
    def mass(self) -> float:
        return self._state.get_mass()

    @ property
    def state(self) -> SpacecraftState:
        return self._state

    @ state.setter
    def state(self, state: SpacecraftState) -> None:
        self._state = state

    @ property
    def controller(self) -> Controller:
        return self._controller

    def get_actuators(self) -> Iterable[Actuator]:
        return [
            self._reaction_wheels,
            self._magnetorquer
        ]

    def get_sensors(self) -> Iterable[Sensor]:
        return [
            self._magnetometer
        ]
