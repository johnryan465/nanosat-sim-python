import math
from datetime import datetime
from typing import List, Tuple, overload

import java.util  # type: ignore
import java.util.stream  # type: ignore
import numpy as np
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
from java.util import Collections  # type: ignore
from java.util.stream import Stream  # type: ignore
from nanosatsim.simulator.utils.units import to_absolute_date
from numpy.typing import NDArray
from org.hipparchus.geometry.euclidean.threed import Vector3D
from org.orekit.bodies import FieldGeodeticPoint, OneAxisEllipsoid
from org.orekit.forces import (AbstractForceModel, ForceModel,
                               PythonForceModel)  # type: ignore
from org.orekit.frames import FramesFactory
from org.orekit.models.earth import GeoMagneticField, GeoMagneticFieldFactory
from org.orekit.propagation import SpacecraftState
from org.orekit.propagation.events import EventDetector
from org.orekit.propagation.numerical import TimeDerivativesEquations
from org.orekit.time import AbsoluteDate, TimeScalesFactory
from org.orekit.utils import Constants, IERSConventions


class MagneticForce(PythonForceModel):
    """
    Here we implement a magnetic force model which will calculate the forces which the
    satillite will experience due to the earths magnetic field and the magnetoquers.


    """

    def __init__(self) -> None:
        super().__init__()

    def init(self, spacecraftState: SpacecraftState, absoluteDate: AbsoluteDate) -> None:
        pass

    @staticmethod
    def get_magnetic_field_vector_ned(date: AbsoluteDate, lla_position: FieldGeodeticPoint) -> Vector3D:
        year = GeoMagneticField.getDecimalYear(date
                                               .getComponents(TimeScalesFactory.getUTC()).getDate().getDay(),
                                               date
                                               .getComponents(TimeScalesFactory.getUTC()).getDate()
                                               .getMonth(),
                                               date
                                               .getComponents(TimeScalesFactory.getUTC()).getDate()
                                               .getYear())

        model = GeoMagneticFieldFactory.getIGRF(year)
        # lat(degrees), long (degrees), alt (km)
        result = model.calculateField(
            lla_position.getLatitude(),
            lla_position.getLongitude(),
            lla_position.getAltitude())

        # magneticFieldVector in ned (measured in - nT - nanoTesla)
        return result.getFieldVector()

    def addContribution(
            self, spacecraftState: SpacecraftState, timeDerivativesEquations: TimeDerivativesEquations) -> None:
        a = self.acceleration(spacecraftState, self.getParameters())
        timeDerivativesEquations.addNonKeplerianAcceleration(a)

    def acceleration(self, s: SpacecraftState, array: List[float]) -> Vector3D:
        """
        tau = mu X B
        """
        date = s.getDate()
        ecf = FramesFactory.getITRF(IERSConventions.IERS_2010, True)
        earth = OneAxisEllipsoid(Constants.WGS84_EARTH_EQUATORIAL_RADIUS, Constants.WGS84_EARTH_FLATTENING, ecf)
        satLatLonAlt = earth.transform(s.getPVCoordinates().getPosition(), FramesFactory.getEME2000(), date)

        date = s.getDate()
        ecf = FramesFactory.getITRF(IERSConventions.IERS_2010, True)
        earth = OneAxisEllipsoid(Constants.WGS84_EARTH_EQUATORIAL_RADIUS, Constants.WGS84_EARTH_FLATTENING, ecf)
        satLatLonAlt = earth.transform(s.getPVCoordinates().getPosition(), FramesFactory.getEME2000(), date)
        if s.hasAdditionalState("dipole_moment"):
            moment_tmp = s.getAdditionalState("dipole_moment")
            moment = Vector3D(moment_tmp[0], moment_tmp[1], moment_tmp[2])
        else:
            moment = Vector3D(0.0, 0.0, 0.0)

        return Vector3D.crossProduct(
            moment,
            MagneticForce.get_magnetic_field_vector_ned(date, satLatLonAlt))

    def dependsOnPositionOnly(self) -> bool:
        return True

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
