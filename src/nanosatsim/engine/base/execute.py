from abc import ABC, abstractmethod
from typing import Any, Dict
from nanosatsim.core.actuator import Actuator
from nanosatsim.core.force import ForceModel
from nanosatsim.core.satellite import Satellite
from nanosatsim.core.sensor import Sensor


class EngineEnviroment(ABC):
    """
    Abstract class for the engine environment.
    """
    @abstractmethod
    def addForceModel(self, force_model: ForceModel) -> None:
        pass

    @abstractmethod
    def addSatillite(self, satellite: Satellite) -> None:
        pass

    @abstractmethod
    def addSensor(self, sensor: Sensor) -> None:
        pass

    @abstractmethod
    def addActuator(self, actuator: Actuator) -> None:
        pass

    @abstractmethod
    def setPosition(self) -> None:
        pass

    @abstractmethod
    def setTime(self) -> None:
        pass


class Engine(ABC):
    """
    Abstract class for the engine.
    """
    @abstractmethod
    def execute(self, environment: EngineEnviroment) -> Dict[str, Any]:
        """
        Execute the engine.
        """
