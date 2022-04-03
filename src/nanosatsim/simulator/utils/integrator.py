from org.hipparchus.ode.nonstiff import DormandPrince853Integrator

from nanosatsim.provider.propagator import NumericalPropagator
from nanosatsim.provider.orbit import Orbit
import orekit
from orekit import JArray_double  # type: ignore


def create_DormandPrince853(initialOrbit: Orbit, minStep: float, maxStep: float, initStep: float,
                            positionTolerance: float) -> DormandPrince853Integrator:
    tolerances = NumericalPropagator.tolerances(positionTolerance,
                                                initialOrbit,
                                                initialOrbit.getType())
    integrator = DormandPrince853Integrator(minStep, maxStep,
                                            JArray_double.cast_(tolerances[0]),
                                            JArray_double.cast_(tolerances[1]))
    integrator.setInitialStepSize(initStep)
    return integrator
