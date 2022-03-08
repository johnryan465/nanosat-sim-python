from typing import Iterable
from enviroment.controller.controller import Controller
from enviroment.satillite.actuators.magnetorquer import SetOfMagnetorquers
from enviroment.satillite.actuators.reactionwheel import SetOfReactionWheels
from enviroment.satillite.sensorsat import SensorSatellite
from enviroment.satillite.state.magnetometer import MagnetometerStateProvider
from enviroment.satillite.state.satellite import SatelliteUpdaterStateProvider


from org.orekit.propagation import SpacecraftState, AdditionalStateProvider
from org.orekit.orbits import Orbit

from enviroment.utils.units import Weight

import numpy.typing as npt
import numpy as np
from numpy import array




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
        self._controller = None

    def get_additional_state_providers(self) -> Iterable[AdditionalStateProvider]:
        state_providers = [
            MagnetometerStateProvider(),
            SatelliteUpdaterStateProvider()
        ]
        return state_providers

    def get_external_torques_magnitude(self) -> float:
        return super().get_external_torques_magnitude()

    def get_set_of_reaction_wheels(self) -> SetOfReactionWheels:
        return super().get_set_of_reaction_wheels()

    def get_I(self) -> npt.NDArray[np.float64]:
        return array([
            [65.77296, 0.002580676, -0.2336325],
            [0.002580676, 56.47602, 0.05447529],
            [-0.2336325, 0.05447529, 16.50073]
        ])

    def get_I_inverse(self) -> npt.NDArray[np.float64]:
        return np.linalg.inv(self.get_I())

    def mass(self) -> float:
        return self._state.getMass()

    def get_set_of_magnetorquers(self) -> SetOfMagnetorquers:
        return super().get_set_of_magnetorquers()

    def state(self) -> SpacecraftState:
        return self._state

    def controller(self) -> Controller:
        return self._controller
