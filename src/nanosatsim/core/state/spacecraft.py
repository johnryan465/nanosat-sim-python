from abc import ABC, abstractmethod
from typing import Generic, TypeVar


Vector = TypeVar("Vector")


class SpacecraftState(Generic[Vector], ABC):
    @abstractmethod
    def get_mass(self) -> float:
        pass

    @abstractmethod
    def get_velocity(self) -> Vector:
        pass

    @abstractmethod
    def get_position(self) -> Vector:
        pass


class AdditionalStateProvider(ABC):
    pass
