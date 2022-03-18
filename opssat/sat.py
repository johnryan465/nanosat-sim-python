from typing import Iterable

import numpy as np
from numpy.typing import NDArray
from numpy import array
from org.orekit.orbits import Orbit
from org.orekit.propagation import AdditionalStateProvider, SpacecraftState
from opssat.actuators.magnetorquer import SetOfMagnetorquers
from opssat.actuators.reactionwheel import SetOfReactionWheels, SetOfReactionWheelsState
from opssat.state.magnetorquer import MagnetorquerStateProvider
from opssat.state.reaction_wheel import ReactionWheelStateProvider
from spacecraft.controller.controller import Controller, SimpleController
from spacecraft.sensorsat import SensorSatellite
from opssat.state.magnetometer import MagnetometerStateProvider


class OPSSAT(SensorSatellite):
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

    def __init__(self, orbit: Orbit) -> None:
        self._state = SpacecraftState(orbit, 5.777673)
        self._controller = SimpleController()
        self._reaction_wheels = SetOfReactionWheels(
            state=SetOfReactionWheelsState(
                control_torque=np.array([0.0, 0.0, 0.0]),
                angular_velocity=np.array([0.0, 0.0, 0.0]),
                inertia=0.0
            )
        )

    def get_additional_state_providers(self) -> Iterable[AdditionalStateProvider]:
        state_providers = [
            MagnetometerStateProvider(),
            MagnetorquerStateProvider(),
            ReactionWheelStateProvider()
        ]
        return state_providers

    def get_inertia(self) -> NDArray[np.float64]:
        return array([
            [65.77296, 0.002580676, -0.2336325],
            [0.002580676, 56.47602, 0.05447529],
            [-0.2336325, 0.05447529, 16.50073]
        ])

    def get_inertia_inverse(self) -> NDArray[np.float64]:
        return np.linalg.inv(self.get_inertia())

    def mass(self) -> float:
        return self._state.getMass()

    @property
    def state(self) -> SpacecraftState:
        return self._state

    @property
    def controller(self) -> Controller:
        return self._controller
