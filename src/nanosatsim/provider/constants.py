from abc import ABC, abstractmethod


class Constants(ABC):
    @property
    @abstractmethod
    def WGS84_EARTH_EQUATORIAL_RADIUS(self) -> float:
        pass

    @property
    @abstractmethod
    def WGS84_EARTH_FLATTENING(self) -> float:
        pass

    @property
    @abstractmethod
    def WGS84_EARTH_MU(self) -> float:
        pass
