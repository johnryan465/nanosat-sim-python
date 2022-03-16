from abc import abstractmethod

import numpy as np
from numpy.typing import NDArray

from spacecraft.actuators.magnetorquer import SetOfMagnetorquers
from spacecraft.actuators.reactionwheel import SetOfReactionWheels
from spacecraft.satellite import Satellite


class SensorSatellite(Satellite):
    @abstractmethod
    def get_external_torques_magnitude(self) -> float:
        pass

    @abstractmethod
    def get_set_of_magnetorquers(self) -> SetOfMagnetorquers:
        pass

    @abstractmethod
    def get_set_of_reaction_wheels(self) -> SetOfReactionWheels:
        pass

    @abstractmethod
    def get_inertia(self) -> NDArray[np.float64]:
        pass

    @abstractmethod
    def get_inertia_inverse(self) -> NDArray[np.float64]:
        pass
