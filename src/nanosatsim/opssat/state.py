from typing import List
from nanosatsim.core.position.orbit import Orbit
from nanosatsim.core.state.spacecraft import SpacecraftState


class OPSSATState(SpacecraftState[List[float]]):
    def __init__(self, mass: float) -> None:
        super().__init__()
        self._mass = mass
        self._velocity = [0.0, 0.0, 0.0]
        self._position = [0.0, 0.0, 0.0]
        self._acceleration = [0.0, 0.0, 0.0]

    def get_mass(self) -> float:
        return self._mass

    def get_velocity(self) -> List[float]:
        return self._velocity

    def get_position(self) -> List[float]:
        return self._position

    def get_acceralation(self) -> List[float]:
        return self._acceleration
