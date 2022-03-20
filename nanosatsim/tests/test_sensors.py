from nanosatsim.spacecraft.sensors.sensors import Sensor


def test_create():
    sensor = Sensor()
    assert isinstance(sensor, Sensor)