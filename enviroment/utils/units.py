from typing import Tuple
from org.orekit.orbits import Orbit 
from org.orekit.orbits import KeplerianOrbit, PositionAngle
from org.orekit.time import AbsoluteDate, TimeScalesFactory
from org.orekit.utils import Constants
from org.orekit.frames import FramesFactory
from math import radians 
from datetime import datetime


def to_absolute_date(date: datetime) -> AbsoluteDate:
    return AbsoluteDate(date.year, date.month, date.day, date.hour, date.minute, float(date.second), TimeScalesFactory.getGPS())


def create_initial_orbit(start_time: datetime) -> Tuple[AbsoluteDate, Orbit]:

    ra = 500 * 1000         #  Apogee
    rp = 400 * 1000         #  Perigee
    i = radians(87.0)      # inclination
    omega = radians(20.0)   # perigee argument
    raan = radians(10.0)  # right ascension of ascending node
    lv = radians(0.0)    # True anomaly

    epochDate = to_absolute_date(start_time)
    initialDate = epochDate

    a = (rp + ra + 2 * Constants.WGS84_EARTH_EQUATORIAL_RADIUS) / 2.0    
    e = 1.0 - (rp + Constants.WGS84_EARTH_EQUATORIAL_RADIUS) / a

    ## Inertial frame where the satellite is defined
    inertialFrame = FramesFactory.getEME2000()

    ## Orbit construction as Keplerian
    initialOrbit = KeplerianOrbit(a, e, i, omega, raan, lv,
                                PositionAngle.TRUE,
                                inertialFrame, epochDate, Constants.WGS84_EARTH_MU)

    return initialDate, initialOrbit


class Weight(float):
    pass
