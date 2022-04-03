from typing import List
from org.orekit.propagation import PythonAdditionalStateProvider  # type: ignore
from org.orekit.propagation import SpacecraftState
from nanosatsim.core.sensor import Sensor


class OrekitSensor(PythonAdditionalStateProvider):
    """
    This class defines a sensor for our satillite,
    these sensors will define a state provider,
    only sensor state providers are available to be
    used by the controllers.
    """

    def __init__(self, sensor: Sensor) -> None:
        super().__init__()
        self.sensor = sensor

    def getAdditionalState(self, state: SpacecraftState) -> List[float]:
        """
        Returns an Orekit State Provider which represents what the sensor records
        """
        return self.sensor.get_new_state(state)

    def getName(self) -> str:
        """
        Return state provider names
        """
        return self.sensor.get_name()
