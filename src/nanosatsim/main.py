from nanosatsim.utils import initial_orekit
from nanosatsim.env import NanosatEnv

initial_orekit()

env = NanosatEnv()
env.render()
