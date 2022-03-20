import orekit
from abc import ABC, abstractmethod
from typing import Iterable
from org.orekit.forces import PythonForceModel  # type: ignore
from org.orekit.frames import FactoryManagedFrame

class Enviroment(ABC):
    @abstractmethod
    def get_force_models(self) -> Iterable[PythonForceModel]:
        """
        Returns an iterable of force models which will apply forces to our satillite
        """


    @abstractmethod
    def get_base_frame(self) -> FactoryManagedFrame:
        """
        Returns the base frame of our enviroment
        """

