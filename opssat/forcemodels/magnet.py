import org.hipparchus
import org.hipparchus.geometry.euclidean.threed
import org.orekit.forces.drag
import org.orekit.forces.empirical
import org.orekit.forces.gravity
import org.orekit.forces.inertia
import org.orekit.forces.maneuvers
import org.orekit.forces.radiation
import org.orekit.frames
import org.orekit.propagation
import org.orekit.propagation.events
import org.orekit.propagation.numerical
import org.orekit.time
import org.orekit.utils
from org.orekit.propagation.events import EventDetector
from org.orekit.propagation import SpacecraftState
from org.orekit.forces import PythonForceModel, AbstractForceModel, ForceModel  # type: ignore
from org.orekit.propagation import SpacecraftState
from org.orekit.time import AbsoluteDate
import java.util
import java.util.stream
from java.util.stream import Stream

from typing import List, overload


class MagneticForce(PythonForceModel):
    """
    Here we implement a magnetic force model which will calculate the forces which the
    satillite will experience due to the earths magnetic field and the magnetoquers.


    """
    def __init__(self) -> None:
        super().__init__()

    def acceleration(self, s: SpacecraftState, array):
        pass

    def addContribution(self, fieldSpacecraftState, fieldTimeDerivativesEquations) -> None:
        pass

    def dependsOnPositionOnly(self) -> bool:
        return True

    def getEventsDetectors(self):
        return Stream.empty()

    def getFieldEventsDetectors(self, field: org.hipparchus.Field):
        pass

    def getParameterDriver(self, string: str) -> org.orekit.utils.ParameterDriver:
        pass

    def getParameters(self) -> List[float]:
        pass

    @overload
    def getParameters(self, field) -> List:
        pass

    def getParametersDrivers(self):
        pass

    def init(self, spacecraftState: SpacecraftState, absoluteDate: AbsoluteDate) -> None:
        pass


    def isSupported(self, string: str) -> bool:
        return True
