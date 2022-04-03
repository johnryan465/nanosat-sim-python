from typing import List
from org.orekit.forces import PythonForceModel  # type: ignore
from org.orekit.propagation.numerical import TimeDerivativesEquations
from org.orekit.time import AbsoluteDate
from org.orekit.models.earth import GeoMagneticFieldFactory
from org.orekit.time import TimeScalesFactory
from org.orekit.bodies import GeodeticPoint
from org.orekit.propagation import SpacecraftState
from org.hipparchus.geometry.euclidean.threed import Vector3D
from org.orekit.utils import Constants
from org.orekit.bodies import OneAxisEllipsoid

from nanosatsim.core.position.frame import Frames


class OrekitMagneticForce(PythonForceModel):
    """
    Here we implement a magnetic force model which will calculate the forces which the
    satillite will experience due to the earths magnetic field and the magnetoquers.
    """

    def __init__(self) -> None:
        super().__init__()

    def init(self, spacecraftState: SpacecraftState, absoluteDate: AbsoluteDate) -> None:
        pass

    @staticmethod
    def get_magnetic_field_vector_ned(date: AbsoluteDate, lla_position: GeodeticPoint) -> Vector3D:
        year = GeoMagneticFieldFactory.getDecimalYear(date
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
        ecf = Frames().getITRF()
        earth = OneAxisEllipsoid(Constants.WGS84_EARTH_EQUATORIAL_RADIUS, Constants.WGS84_EARTH_FLATTENING, ecf)
        satLatLonAlt = earth.transform(s.getPVCoordinates().getPosition(), Frames().getEME2000(), date)

        date = s.getDate()
        ecf = Frames().getITRF()
        earth = OneAxisEllipsoid(Constants.WGS84_EARTH_EQUATORIAL_RADIUS, Constants.WGS84_EARTH_FLATTENING, ecf)
        satLatLonAlt = earth.transform(s.getPVCoordinates().getPosition(), Frames().getEME2000(), date)
        if s.hasAdditionalState("dipole_moment"):
            moment_tmp = s.getAdditionalState("dipole_moment")
            moment = Vector3D(moment_tmp[0], moment_tmp[1], moment_tmp[2])
        else:
            moment = Vector3D(0.0, 0.0, 0.0)

        return Vector3D.crossProduct(
            moment,
            OrekitMagneticForce.get_magnetic_field_vector_ned(date, satLatLonAlt))
