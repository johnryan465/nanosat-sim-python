from datetime import datetime
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
from org.orekit.models.earth import GeoMagneticFieldFactory
from org.orekit.models.earth import GeoMagneticField
from org.orekit.time import TimeScalesFactory
from numpy.typing import NDArray
from org.orekit.bodies import OneAxisEllipsoid
from org.orekit.frames import FramesFactory
from org.orekit.utils import IERSConventions, Constants
from org.orekit.bodies import FieldGeodeticPoint
import numpy as np
import math
from enviroment.utils.units import to_absolute_date
import java.util
import java.util.stream
from java.util import Collections
from java.util.stream import Stream

from org.hipparchus.geometry.euclidean.threed import Vector3D


from typing import List, Tuple, overload


class MagneticForce(PythonForceModel):
    """
    Here we implement a magnetic force model which will calculate the forces which the
    satillite will experience due to the earths magnetic field and the magnetoquers.


    """

    def __init__(self) -> None:
        pass

    def get_magnetic_field_vector_ned(self, date: AbsoluteDate, lla_position: FieldGeodeticPoint) -> Vector3D:
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

    def get_satillite_mag_field(self) -> Vector3D:
        return Vector3D(0.0, 0.0, 0.0)

    def acceleration(self, s: SpacecraftState, array: List[float]) -> Vector3D:
        """
        tau = mu X B
        """
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
            self.get_magnetic_field_vector_ned(date, satLatLonAlt))

    def dependsOnPositionOnly(self) -> bool:
        return True

    def getEventsDetectors(self):
        return Stream.empty()

    def getFieldEventsDetectors(self, field: org.hipparchus.Field):
        return Stream.empty()

    def getParametersDrivers(self):
        return Collections.emptyList()

    def isSupported(self, string: str) -> bool:
        return False
