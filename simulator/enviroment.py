from abc import ABC, abstractmethod
from typing import Iterable
from org.orekit.forces import PythonForceModel  # type: ignore


class Enviroment(ABC):
    @abstractmethod
    def get_force_models(self) -> Iterable[PythonForceModel]:
        pass

