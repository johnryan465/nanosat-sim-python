from typing import List
from org.orekit.forces import PythonForceModel  # type: ignore
import java.util  # type: ignore
import java.util.stream  # type: ignore
from java.util import Collections  # type: ignore
from java.util.stream import Stream  # type: ignore
import org.hipparchus


class ForceModel(PythonForceModel):
    def dependsOnPositionOnly(self) -> bool:
        return False

    def getEventsDetectors(self):
        return Stream.empty()

    def getFieldEventsDetectors(self, field: org.hipparchus.Field):
        return Stream.empty()

    def getParametersDrivers(self):
        return Collections.emptyList()

    def getParameters(self) -> List[float]:
        return []

    def isSupported(self, string: str) -> bool:
        return False
