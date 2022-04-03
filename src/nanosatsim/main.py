from nanosatsim.opssat.env import OPSSATEnv
from nanosatsim.opssat.satellite import OPSSAT
from nanosatsim.simulator.enviroment import SpaceEnviroment
from nanosatsim.simulator.main import Simulator
from nanosatsim.utils import initial_orekit

initial_orekit()


if __name__ == '__main__':
    env = OPSSATEnv()
    satellite = OPSSAT()
    simulator = Simulator(satellite, env, 0.1)
    print(simulator.run())
