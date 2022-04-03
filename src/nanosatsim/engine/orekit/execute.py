from dataclasses import dataclass
from typing import Any, Dict
from nanosatsim.core.actuator import Actuator
from nanosatsim.core.force import ForceModel
from nanosatsim.core.force.gravity import HolmesFeatherstoneAttractionModel
from nanosatsim.core.force.magnet import GeoMagneticField
from nanosatsim.core.position.frame import Frames
from nanosatsim.core.position.orbit import Orbit, OrbitType
from nanosatsim.core.satellite import Satellite
from nanosatsim.core.sensor import Sensor
from nanosatsim.engine.base.execute import Engine, EngineEnviroment
from nanosatsim.engine.orekit.actuator import OrekitActuator
from nanosatsim.engine.orekit.magnet import OrekitMagneticForce
from nanosatsim.engine.orekit.sensor import OrekitSensor
from nanosatsim.engine.orekit.utils.integrator import create_DormandPrince853
from org.orekit.propagation.numerical import NumericalPropagator
from org.orekit.forces.gravity import HolmesFeatherstoneAttractionModel as OrekitHolmesFeatherstoneAttractionModel
from org.orekit.forces.gravity.potential import GravityFieldFactory as OrekitGravityFieldFactory
from org.orekit.utils import Constants
from org.orekit.time import TimeScalesFactory, AbsoluteDate
from org.orekit.utils import IERSConventions
from org.hipparchus.geometry.euclidean.threed import Vector3D
from org.orekit.orbits import KeplerianOrbit
from org.orekit.frames import FramesFactory
from org.orekit.propagation import SpacecraftState
from org.orekit.utils import PVCoordinates


@dataclass
class IntegratorConfig:
    min_step: float = 0.001
    max_step: float = 1000.0
    init_step: float = 60.0
    position_tolerance: float = 1.0


class OrekitEngineEnviroment(EngineEnviroment):
    """
    Abstract class for the engine environment.
    """

    def __init__(self) -> None:
        super().__init__()
        self.start_date = AbsoluteDate(2014, 1, 1, 23, 30, 00.000, TimeScalesFactory.getUTC())
        position = Vector3D(-6142438.668, 3492467.560, -25767.25680)
        velocity = Vector3D(505.8479685, 942.7809215, 7435.922231)
        self.orbit = KeplerianOrbit(PVCoordinates(position, velocity),
                                    FramesFactory.getEME2000(), self.start_date,
                                    Constants.EIGEN5C_EARTH_MU)
        self.int_config = IntegratorConfig()
        integrator = create_DormandPrince853(self.orbit,
                                             self.int_config.min_step,
                                             self.int_config.max_step,
                                             self.int_config.init_step,
                                             self.int_config.position_tolerance)
        orbit_type = OrbitType.CARTESIAN

        # We need to initialise the propagator
        self.propagator = NumericalPropagator(integrator)
        self.propagator.setOrbitType(orbit_type)

    def addForceModel(self, force_model: ForceModel) -> None:
        if isinstance(force_model, HolmesFeatherstoneAttractionModel):
            itrf = Frames().getITRF()
            gravity_provider = OrekitGravityFieldFactory.getNormalizedProvider(8, 8)
            gravity_force_model = OrekitHolmesFeatherstoneAttractionModel(itrf, gravity_provider)
            orekit_force_model = gravity_force_model
        elif isinstance(force_model, GeoMagneticField):
            orekit_force_model = OrekitMagneticForce()
        else:
            raise NotImplementedError("Force model not implemented")

        self.propagator.addForceModel(orekit_force_model)

    def addSatillite(self, satellite: Satellite) -> None:
        orekit_satellite = SpacecraftState(self.orbit, 5.777673)
        self.propagator.setInitialState(orekit_satellite)

    def addSensor(self, sensor: Sensor) -> None:
        orekit_sensor = OrekitSensor(sensor)
        print(orekit_sensor)
        self.propagator.addAdditionalStateProvider(orekit_sensor)

    def addActuator(self, actuator: Actuator) -> None:
        orekit_actuator = OrekitActuator(actuator)
        self.propagator.addAdditionalStateProvider(orekit_actuator)

    def setPosition(self) -> None:
        return None

    def setTime(self) -> None:
        return None


class OrekitEngine(Engine):
    """
    Abstract class for the engine.
    """

    def execute(self, environment: EngineEnviroment) -> Dict[str, Any]:
        """
        Execute the engine.
        """
        assert isinstance(environment, OrekitEngineEnviroment)
        new_date = environment.start_date.shiftedBy(60.0)
        return environment.propagator.propagate(new_date)
