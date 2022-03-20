from abc import abstractmethod

import numpy as np
from numpy.typing import NDArray


from nanosatsim.spacecraft.satellite import Satellite


class SensorSatellite(Satellite):
    @abstractmethod
    def get_inertia(self) -> NDArray[np.float64]:
        pass

    @abstractmethod
    def get_inertia_inverse(self) -> NDArray[np.float64]:
        pass
