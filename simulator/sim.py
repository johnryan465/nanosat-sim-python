from datetime import datetime
from typing import Optional


from org.orekit.attitudes import Attitude
from org.orekit.bodies import OneAxisEllipsoid
from org.orekit.forces.gravity import HolmesFeatherstoneAttractionModel
from org.orekit.forces.gravity.potential import GravityFieldFactory
from org.orekit.frames import FramesFactory
from org.orekit.orbits import Orbit, OrbitType
from org.orekit.propagation.numerical import NumericalPropagator
from org.orekit.propagation.sampling import \
    OrekitFixedStepHandler, PythonOrekitFixedStepHandler  # type: ignore
from org.orekit.time import AbsoluteDate
from org.orekit.utils import Constants, IERSConventions
from spacecraft.sensorsat import SensorSatellite

# from simulator.kinematics import Kinematics
# from simulator.kinetics import Kinetics

from enviroment.force.magnet import MagneticForce
from enviroment.utils.integrator import create_DormandPrince853
from enviroment.utils.units import to_absolute_date

class Step(PythonOrekitFixedStepHandler):
    eclipseAngles = []
    pointingOffsets = []
    dates = []
    
class Simulator:
    def __init__(self, satellite: SensorSatellite, orbit: Orbit, initial_attitude: Attitude) -> None:
        self.initial_state = satellite.state()
        self.satellite = satellite
        self.orbit: Orbit = orbit
        self.initial_attitude: Attitude = initial_attitude
        self.step: Optional[float] = 1.
        self.start_time: AbsoluteDate = initial_attitude.getDate()
        self.step_handler: Optional[OrekitFixedStepHandler] = Step()


    def run(self, end_time: datetime) -> None:
        """
        Run the simulatotion
        
        """
        end_time = to_absolute_date(end_time)
        # kinematics_attitude_provider = Kinematics(self.initial_attitude, self.satellite)
        # kinetics_attitude_modifier = Kinetics(kinematics_attitude_provider, self.satellite)
        # controller_modifier = ControllerAttitude(kinetics_attitude_modifier, self.satellite)

        # at = InertialProvider.of(self.orbit.getFrame())

        print(self.orbit)
        min_step = 0.001
        max_step = 1000.0
        init_step = 60.0
        integrator = create_DormandPrince853(self.orbit, min_step, max_step, init_step, 1.0)
        orbit_type = OrbitType.CARTESIAN
        propagator = NumericalPropagator(integrator)
        propagator.setOrbitType(orbit_type)
        propagator.setInitialState(self.initial_state)

        itrf  = FramesFactory.getITRF(IERSConventions.IERS_2010, True) # International Terrestrial Reference Frame, earth fixed
        earth = OneAxisEllipsoid(Constants.WGS84_EARTH_EQUATORIAL_RADIUS,
                         Constants.WGS84_EARTH_FLATTENING,
                         itrf)
        gravityProvider = GravityFieldFactory.getNormalizedProvider(8, 8)
        propagator.addForceModel(HolmesFeatherstoneAttractionModel(earth.getBodyFrame(), gravityProvider))
        propagator.addForceModel(MagneticForce())

        # propagator.setMasterMode(180.0, handler) 
        # propagator.setInitialState(initialState)
        for additional_state in self.satellite.get_additional_state_providers():
            print(additional_state)
            # propagator.addAdditionalStateProvider(additional_state)

        if self.step_handler is not None and self.step is not None:
            # propagator.setStepHandler(self.step, self.step_handler)
            print(3)
        print(self.initial_state)
        state = propagator.propagate(end_time)
        print(state)
