from nanosatsim.spacecraft.sensors import Sensor
from nanosatsim.utils import initial_orekit


def test_create():
    initial_orekit()
    sensor = Sensor()
    assert isinstance(sensor, Sensor)
