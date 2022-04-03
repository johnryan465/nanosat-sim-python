from nanosatsim.engine.base.execute import Engine, EngineEnviroment
from nanosatsim.core.satellite import Satellite
from nanosatsim.engine.orekit.execute import OrekitEngine, OrekitEngineEnviroment
from nanosatsim.core.enviroment import SpaceEnviroment
from nanosatsim.core.state.spacecraft import SpacecraftState as _SpacecraftState
from typing import Any, Dict, Generic, TypeVar


SpacecraftState = TypeVar('SpacecraftState', bound=_SpacecraftState)


class Simulator(Generic[SpacecraftState]):
    def __init__(self, satellite: Satellite, env: SpaceEnviroment, step_size: float) -> None:
        self.env = env
        self.satellite = satellite
        self.step_size = step_size
        self.engine: Engine = OrekitEngine()

    def run(self) -> Dict[str, Any]:
        """
        Run the simulatition with the initial state, until the end time.
        """

        engine_env: EngineEnviroment = OrekitEngineEnviroment()
        engine_env.addSatillite(self.satellite)

        # The additional state providers will create state which our force models can use
        # This distintion lets us have much cleaner distintiions.

        for sensor in self.satellite.get_sensors():
            engine_env.addSensor(sensor)

        for actuator in self.satellite.get_actuators():
            engine_env.addActuator(actuator)

        # The force models will read the state and then use that to update the acceleration.
        for force_model in self.env.get_force_models():
            engine_env.addForceModel(force_model)

        return self.engine.execute(engine_env)
