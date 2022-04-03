from dataclasses import dataclass
from typing import List, Tuple
import torch
from gym.spaces import Box
import numpy as np

from astropy import coordinates
from astropy.units import Quantity


class BaseSpace:
    def get_sensors(self) -> List[Tuple[str, Quantity]]:
        l = []
        for name, sensor in sorted(vars(self).items()):
            if isinstance(sensor, Quantity):
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
    reaction_wheel_x: Quantity["angular velocity"]
    reaction_wheel_y: Quantity["angular velocity"]
    reaction_wheel_z: Quantity["angular velocity"]
    magnetorquer_x: Quantity["tesla"]
    magnetorquer_y: Quantity["tesla"]
    magnetorquer_z: Quantity["tesla"]


@dataclass
class SatObservationSpace(BaseSpace):
    latitude: coordinates.Latitude
    longitude: coordinates.Longitude
    altitude: coordinates.Distance
    mag_field_r: Quantity["tesla"]
    mag_field_b: Quantity["tesla"]
    accel_x: Quantity["angular acceleration"]
    accel_Y: Quantity["angular acceleration"]
    accel_Z: Quantity["angular acceleration"]
