"""
This module is designed to visualise the outputs of the simulator
"""
from orekit.pyhelpers import setup_orekit_curdir
import orekit
from nanosatsim.simulator.main import Simulator
from nanosatsim.opssat.sat import OPSSAT
from nanosatsim.opssat.env import OPSSATEnv
from nanosatsim.provider.vector import Vector
from nanosatsim.provider.orbit import KeplerianOrbit
from nanosatsim.provider.frame import Frames
from nanosatsim.provider.constants import Constants
from nanosatsim.provider.time import AbsoluteDate, TimeScalesFactory
from nanosatsim.provider.coordinates import PVCoordinates


def create_orbit():
    initialDate = AbsoluteDate(2004, 1, 1, 23, 30, 00.000, TimeScalesFactory.getUTC())
    position = Vector(-6142438.668, 3492467.560, -25767.25680)
    velocity = Vector(5050.8479685, 942.7809215, 7435.922231)
    initialOrbit = KeplerianOrbit(PVCoordinates(position, velocity),
                                  Frames().getEME2000(), initialDate,
                                  Constants.EIGEN5C_EARTH_MU)
    return initialOrbit


if __name__ == "__main__":
    vm = orekit.initVM()  # type: ignore
    setup_orekit_curdir()
    orbit = create_orbit()
    opssat = OPSSAT(orbit=orbit)
    env = OPSSATEnv()
    simulator = Simulator(satellite=opssat, orbit=orbit, env=env, step_size=60.0 * 60 * 24)
    end_date = AbsoluteDate(2004, 2, 1, 23, 30, 00.000, TimeScalesFactory.getUTC())
    print(simulator.run(end_date))
