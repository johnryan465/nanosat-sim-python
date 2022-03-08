from abc import abstractmethod
from enviroment.satillite.actuators.magnetorquer import SetOfMagnetorquers
from enviroment.satillite.actuators.reactionwheel import SetOfReactionWheels
from enviroment.satillite.satellite import Satellite
import numpy.typing as npt
import numpy as np


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
    def get_I(self) -> npt.NDArray[np.float64]:
        pass

    @abstractmethod
    def get_I_inverse(self) -> npt.NDArray[np.float64]:
        pass
