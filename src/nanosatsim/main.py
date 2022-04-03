from nanosatsim.opssat.env import OPSSATEnv
from nanosatsim.opssat.satellite import OPSSAT
from nanosatsim.simulator import Simulator
from nanosatsim.utils import initial_orekit


if __name__ == '__main__':
    initial_orekit()
    env = OPSSATEnv()
    satellite = OPSSAT()
    simulator = Simulator(satellite, env, 0.1)
    print(simulator.run())
