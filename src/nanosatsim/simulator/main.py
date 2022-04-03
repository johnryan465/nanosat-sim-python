from nanosatsim.provider import Provider
from nanosatsim.provider.propagator import NumericalPropagator
from nanosatsim.simulator.utils.integrator import create_DormandPrince853
from nanosatsim.spacecraft.sensorsat import SensorSatellite
from nanosatsim.simulator.enviroment import Enviroment
from nanosatsim.provider.orbit import Orbit, OrbitType
from nanosatsim.provider.time import AbsoluteDate
from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class IntegratorConfig:
    min_step: float = 0.001
    max_step: float = 1000.0
    init_step: float = 60.0
    position_tolerance: float = 1.0


class Simulator:
    def __init__(self, satellite: SensorSatellite, orbit: Orbit, env: Enviroment, step_size: float, provider: Provider) -> None:
        self.env = env
        self.satellite = satellite
        self.orbit = orbit
        self.step_size = step_size
        self.int_config = IntegratorConfig()
        self.provider = provider

    def initialise_satellite(self) -> None:
        pass

    def run(self, end_time: AbsoluteDate) -> Dict[str, Any]:
        """
        Run the simulatition with the initial state, until the end time.
        """
        integrator = create_DormandPrince853(self.orbit, self.int_config.min_step,
                                             self.int_config.max_step, self.int_config.init_step, self.int_config.position_tolerance)
        orbit_type = OrbitType.CARTESIAN

        # We need to initialise the propagator
        propagator = NumericalPropagator(integrator)
        propagator.setOrbitType(orbit_type)
        propagator.setInitialState(self.satellite.state)

        # The additional state providers will create state which our force models can use
        # This distintion lets us have much cleaner distintiions.

        for sensor in self.satellite.get_sensors():
            propagator.addAdditionalStateProvider(sensor)

        for actuator in self.satellite.get_actuators():
            propagator.addAdditionalStateProvider(actuator)

        # The force models will read the state and then use that to update the acceleration.
        for force_model in self.env.get_force_models():
            propagator.addForceModel(force_model)

        states = []
        extrap_date = self.satellite.state.getDate()
        while extrap_date.compareTo(end_time) <= 0.0:
            state = propagator.propagate(extrap_date)
            states.append(state)
            extrap_date = extrap_date.shiftedBy(self.step_size)

        return {
            "state": states
        }
