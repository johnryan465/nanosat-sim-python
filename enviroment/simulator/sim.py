from datetime import datetime
import imp
from typing import Optional
from org.orekit.attitudes import Attitude, InertialProvider

from org.orekit.propagation.numerical import NumericalPropagator
from org.orekit.propagation.analytical import EcksteinHechlerPropagator, KeplerianPropagator
from org.orekit.propagation.sampling import PythonOrekitFixedStepHandler
from org.orekit.orbits import Orbit
from enviroment.controller.attitude import ControllerAttitude

from enviroment.satillite.sensorsat import SensorSatellite
from enviroment.simulator.kinematics import Kinematics
from enviroment.simulator.kinetics import Kinetics
# from enviroment.simulator.keplerian import KeplerianPropagator
from org.orekit.time import AbsoluteDate, UTCScale
from org.orekit.time import TimeScalesFactory
from org.orekit.orbits import OrbitType
from org.orekit.utils import Constants

from enviroment.utils.integrator import create_DormandPrince853

def _to_absolute_date(date: datetime) -> AbsoluteDate:
    return AbsoluteDate(date.year, date.month, date.day, date.hour, date.minute, float(date.second), TimeScalesFactory.getGPS())


class Step(PythonOrekitFixedStepHandler):
    
    eclipseAngles = []
    pointingOffsets = []
    dates = []
    
    def init(self,s0, t, step):
        pass
        
    def handleStep(self, currentState, isLast):
        print(1)

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
        end_time = _to_absolute_date(end_time)
        kinematics_attitude_provider = Kinematics(self.initial_attitude, self.satellite)
        kinetics_attitude_modifier = Kinetics(kinematics_attitude_provider, self.satellite)
        controller_modifier = ControllerAttitude(kinetics_attitude_modifier, self.satellite)

        at = InertialProvider.of(self.orbit.getFrame())

        print(self.orbit)
        minStep = 0.001;
        maxstep = 1000.0;
        initStep = 60.0
        integrator = create_DormandPrince853(self.orbit, minStep, maxstep, initStep, 1.0)
        orbitType = OrbitType.CARTESIAN
        propagator = KeplerianPropagator(self.orbit, kinematics_attitude_provider) #, kinematics_attitude_provider)
        # propagator = EcksteinHechlerPropagator(self.orbit, kinematics_attitude_provider,
        #                                                    Constants.EIGEN5C_EARTH_EQUATORIAL_RADIUS,
        #                                                    Constants.EIGEN5C_EARTH_MU, Constants.EIGEN5C_EARTH_C20,
        #                                                    Constants.EIGEN5C_EARTH_C30, Constants.EIGEN5C_EARTH_C40,
        #                                                    Constants.EIGEN5C_EARTH_C50, Constants.EIGEN5C_EARTH_C60)
        # propagator = NumericalPropagator(integrator, kinematics_attitude_provider)
        # propagator.setOrbitType(orbitType)
        # propagator.setInitialState(self.initial_state)
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
