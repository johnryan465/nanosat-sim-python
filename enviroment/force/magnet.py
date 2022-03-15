import java.util
import java.util.stream
from java.util.stream import Stream
from enviroment.force.force import Force
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
from org.orekit.forces import PythonForceModel, AbstractForceModel, ForceModel
from org.orekit.propagation import SpacecraftState
from org.orekit.time import AbsoluteDate
import typing

class MagneticForce(PythonForceModel):
    def __init__(self) -> None:
        super().__init__()

    def acceleration(self, spacecraftState, array):
        pass

    def addContribution(self, fieldSpacecraftState, fieldTimeDerivativesEquations) -> None:
        pass

    def dependsOnPositionOnly(self) -> bool:
        pass

    def getEventsDetectors(self):
        return Stream.empty()

    def getFieldEventsDetectors(self, field: org.hipparchus.Field):
        pass

    def getParameterDriver(self, string: str) -> org.orekit.utils.ParameterDriver:
        pass

    def getParameters(self) -> typing.List[float]:
        pass

    @typing.overload
    def getParameters(self, field) -> typing.List:
        pass

    def getParametersDrivers(self):
        pass

    def init(self, spacecraftState: org.orekit.propagation.SpacecraftState, absoluteDate: org.orekit.time.AbsoluteDate) -> None:
        pass


    def isSupported(self, string: str) -> bool:
        return True
