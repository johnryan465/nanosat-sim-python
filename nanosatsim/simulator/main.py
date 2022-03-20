from datetime import datetime
from typing import Any, Dict
import numpy as np
from numpy.typing import NDArray


from org.orekit.attitudes import Attitude
from org.orekit.orbits import Orbit, OrbitType
from org.orekit.propagation.numerical import NumericalPropagator
from org.orekit.propagation.sampling import \
    OrekitFixedStepHandler, PythonOrekitFixedStepHandler  # type: ignore
from org.orekit.time import AbsoluteDate
from nanosatsim.simulator.enviroment import Enviroment
from nanosatsim.spacecraft.sensorsat import SensorSatellite

from nanosatsim.simulator.utils.integrator import create_DormandPrince853
from nanosatsim.simulator.utils.units import to_absolute_date


class Simulator:
    def __init__(self, satellite: SensorSatellite, orbit: Orbit, env: Enviroment, step_size: float) -> None:
        self.env = env
        self.satellite = satellite
        self.orbit = orbit
        self.step_size = step_size

    def initialise_satellite(self) -> None:
        pass

    def run(self, end_time: AbsoluteDate) -> Dict[str, Any]:
        """
        Run the simulatition with the initial state, until the end time.
        """
        print(self.satellite.state)

        min_step = 0.001
        max_step = 1000.0
        init_step = 60.0
        integrator = create_DormandPrince853(self.orbit, min_step, max_step, init_step, 1.0)
        orbit_type = OrbitType.CARTESIAN

        # We need to initialise the propagator
        propagator = NumericalPropagator(integrator)
        propagator.setOrbitType(orbit_type)
        propagator.setInitialState(self.satellite.state)

        # The additional state providers will create state which our force models can use
        # This distintion lets us have much cleaner distintiions.

        for additional_state in self.satellite.get_additional_state_providers():
            propagator.addAdditionalStateProvider(additional_state)

        # The force models will read the state and then use that to update the acceleration.
        for force_model in self.env.get_force_models():
            propagator.addForceModel(force_model)

        states = []
        extrapDate = self.satellite.state.getDate()
        while (extrapDate.compareTo(end_time) <= 0.0):
            state = propagator.propagate(extrapDate)
            states.append(state)
            extrapDate = extrapDate.shiftedBy(self.step_size)

        return {
            "state": states
        }
