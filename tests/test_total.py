from nanosatsim.provider.coordinates import PVCoordinates


from nanosatsim.provider.constants import Constants
from nanosatsim.provider.frame import Frames
from nanosatsim.provider.orbit import KeplerianOrbit
from nanosatsim.opssat.env import OPSSATEnv
from nanosatsim.opssat.sat import OPSSAT
from nanosatsim.simulator.main import Simulator
from nanosatsim.utils import initial_orekit
from nanosatsim.provider.time import AbsoluteDate, TimeScalesFactory
from nanosatsim.provider.vector import Vector


def create_orbit(initialDate: AbsoluteDate):
    position = Vector(-6142438.668, 3492467.560, -25767.25680)
    velocity = Vector(505.8479685, 942.7809215, 7435.922231)
    initialOrbit = KeplerianOrbit(PVCoordinates(position, velocity),
                                  Frames().getEME2000(), initialDate,
                                  Constants.EIGEN5C_EARTH_MU)
    return initialOrbit


def test_run():
    initial_orekit()
    start_date = AbsoluteDate(2014, 1, 1, 23, 30, 00.000, TimeScalesFactory.getUTC())
    orbit = create_orbit(start_date)
    opssat = OPSSAT(orbit=orbit)
    env = OPSSATEnv()
    simulator = Simulator(satellite=opssat, orbit=orbit, env=env, step_size=60.0 * 60)
    end_date = AbsoluteDate(2014, 2, 1, 23, 40, 00.000, TimeScalesFactory.getUTC())
    res = simulator.run(end_date)
