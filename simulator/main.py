from datetime import datetime
from typing import Dict
import numpy as np
from numpy.typing import NDArray


from org.orekit.attitudes import Attitude
from org.orekit.orbits import Orbit, OrbitType
from org.orekit.propagation.numerical import NumericalPropagator
from org.orekit.propagation.sampling import \
    OrekitFixedStepHandler, PythonOrekitFixedStepHandler  # type: ignore
from org.orekit.time import AbsoluteDate
from simulator.enviroment import Enviroment
from spacecraft.sensorsat import SensorSatellite

from enviroment.utils.integrator import create_DormandPrince853
from enviroment.utils.units import to_absolute_date

    
class Simulator:
    def __init__(self, satellite: SensorSatellite, orbit: Orbit, initial_attitude: Attitude, env: Enviroment) -> None:
        self.initial_state = satellite.state()
        self.env = env
        self.satellite = satellite
        self.orbit: Orbit = orbit
        self.initial_attitude: Attitude = initial_attitude
        self.start_time: AbsoluteDate = initial_attitude.getDate()

    def initialise_satellite(self) -> None:
        pass

    def run(self, end_time: datetime) -> Dict[str, NDArray[np.float64]]:
        """
        Run the simulatition with the initial state, until the end time.
        """
        end_time = to_absolute_date(end_time)

        min_step = 0.001
        max_step = 1000.0
        init_step = 60.0
        integrator = create_DormandPrince853(self.orbit, min_step, max_step, init_step, 1.0)
        orbit_type = OrbitType.CARTESIAN


        # We need to initialise the propagator
        propagator = NumericalPropagator(integrator)
        propagator.setOrbitType(orbit_type)
        propagator.setInitialState(self.initial_state)


        # The additional state providers will create state which our force models can use
        # This distintion lets us have much cleaner distintiions.

        for additional_state in self.satellite.get_additional_state_providers():
            propagator.addAdditionalStateProvider(additional_state)


        # The force models will read the state and then use that to update the acceleration.
        for force_model in self.env.get_force_models():
            propagator.addForceModel(force_model)

        state = propagator.propagate(end_time)

        return {
            "state": state
        }
