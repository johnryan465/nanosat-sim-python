"""
This module is designed to visualise the outputs of the simulator
"""
from opssat.env import OPSSATEnv
from opssat.sat import OPSSAT
from simulator.main import Simulator

import orekit
from orekit.pyhelpers import setup_orekit_curdir
from orekit.pyhelpers import absolutedate_to_datetime 

from org.orekit.frames import FramesFactory
from org.orekit.orbits import KeplerianOrbit
from org.orekit.time import AbsoluteDate
from org.orekit.time import TimeScalesFactory
from org.orekit.utils import Constants, IERSConventions, AngularDerivativesFilter
from org.orekit.utils import PVCoordinates
from org.hipparchus.geometry.euclidean.threed import Vector3D


def create_orbit():
    initialDate =  AbsoluteDate(2004, 1, 1, 23, 30, 00.000, TimeScalesFactory.getUTC())
    position  = Vector3D(-6142438.668, 3492467.560, -25767.25680);
    velocity  = Vector3D(5050.8479685, 942.7809215, 7435.922231);
    initialOrbit =  KeplerianOrbit(PVCoordinates(position, velocity),
                                                            FramesFactory.getEME2000(), initialDate,
                                                            Constants.EIGEN5C_EARTH_MU);
    return initialOrbit

if __name__ == "__main__":
    vm = orekit.initVM()
    setup_orekit_curdir()
    orbit = create_orbit()
    opssat = OPSSAT(orbit=orbit)
    env = OPSSATEnv()
    simulator = Simulator(satellite=opssat, orbit=orbit, env=env)
    end_date = AbsoluteDate(2004, 2, 1, 23, 30, 00.000, TimeScalesFactory.getUTC())
    print(simulator.run(end_date))