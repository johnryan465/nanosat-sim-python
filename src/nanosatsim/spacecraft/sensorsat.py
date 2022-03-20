from abc import abstractmethod
from typing import Iterable
from nanosatsim.spacecraft.actuators import Actuator


from nanosatsim.spacecraft.satellite import Satellite
from nanosatsim.spacecraft.sensors import Sensor


class SensorSatellite(Satellite):
    @abstractmethod
    def get_sensors(self) -> Iterable[Sensor]:
        """
        This returns a list of sensors which the satillite has
        """

    @abstractmethod
    def get_actuators(self) -> Iterable[Actuator]:
        """
        This returns a list of actuators
        """
