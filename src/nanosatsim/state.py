from abc import ABC, abstractmethod, abstractproperty
from dataclasses import dataclass
from enum import Enum
from typing import Callable, Generic, List, Tuple, TypeVar

from gym.spaces import Box
from nanosatsim.units import Radians, Units, Tesla, AngularVelocity, Degrees, Metres, Time, Acceleration
import torch
import numpy as np


Unit = TypeVar("Unit", bound=Units)
Value = TypeVar("Value")


@dataclass
class SensorValue(Generic[Value, Unit]):
    """
    Value of the sensor with unit
    """
    unit: Unit
    low: Value
    high: Value
    value: Value


class MagnetorquerValue(SensorValue[float, Tesla]):
    unit = Tesla()
    low = 0.0
    high = 1.0

    def __init__(self, value: float):
        self.value = value


class MagnetometerValue(SensorValue[float, Tesla]):
    unit = Tesla()
    low = 0.0
    high = 1.0

    def __init__(self, value: float):
        self.value = value


class ReactionWheelValue(SensorValue[float, AngularVelocity]):
    unit = AngularVelocity()
    low = 0.0
    high = 1.0

    def __init__(self, value: float):
        self.value = value


class AccelerationValue(SensorValue[float, Acceleration]):
    unit = Acceleration()
    low = 0.0
    high = 1.0

    def __init__(self, value: float):
        self.value = value


class DegreesValue(SensorValue[float, Degrees]):
    unit = Degrees()
    low = -180.0
    high = 180.0

    def __init__(self, value: float):
        self.value = value


class RadiansValue(SensorValue[float, Radians]):
    unit = Radians()
    low = -4
    high = 4

    def __init__(self, value: float):
        self.value = value


class MetresValue(SensorValue[float, Metres]):
    unit = Metres()
    low = 0.0
    high = 100000.0

    def __init__(self, value: float):
        self.value = value


@dataclass
class BaseSpace:
    def get_sensors(self) -> List[Tuple[str, SensorValue]]:
        l = []
        for name, sensor in sorted(vars(self).items()):
            if isinstance(sensor, SensorValue):
                l.append((name, sensor))
        return l

    def to_tensor(self) -> torch.Tensor:
        return torch.tensor([v.value for n, v in self.get_sensors()])

    def to_mapping(self) -> List[str]:
        return list([n for n, _ in self.get_sensors()])

    def bound(self) -> Box:
        l = list([(v.low, v.high) for _, v in self.get_sensors()])
        low, high = zip(*l)
        return Box(low=np.array(low), high=np.array(high))


@dataclass
class SatActionSpace(BaseSpace):
    reaction_wheel_x: SensorValue[float, AngularVelocity]
    reaction_wheel_y: SensorValue[float, AngularVelocity]
    reaction_wheel_z: SensorValue[float, AngularVelocity]
    magnetorquer_x:  SensorValue[float, Tesla]
    magnetorquer_y:  SensorValue[float, Tesla]
    magnetorquer_z:  SensorValue[float, Tesla]


@dataclass
class SatObservationSpace(BaseSpace):
    latitude: SensorValue[float, Radians]
    longitude: SensorValue[float, Radians]
    altitude: SensorValue[float, Metres]
    mag_field_r: SensorValue[float, Tesla]
    mag_field_b: SensorValue[float, Tesla]
    accel_x: SensorValue[float, Acceleration]
    accel_Y: SensorValue[float, Acceleration]
    accel_Z: SensorValue[float, Acceleration]
