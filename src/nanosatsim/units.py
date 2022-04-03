from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Units(ABC):
    """
    Unit Type
    """
    name: str = ""
    short: str = ""


class Tesla(Units):
    name: str = "telsa"
    short: str = "t"


class AngularVelocity(Units):
    name: str = "angular"
    short: str = "w/s"


class Acceleration(Units):
    name: str = "acceleration"
    short: str = "m/s^2"


class Degrees(Units):
    pass


class Radians(Units):
    pass


class Metres(Units):
    pass


class Time(Units):
    pass
