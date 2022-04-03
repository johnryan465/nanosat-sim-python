from nanosatsim.core.force.force_model import ForceModel
from nanosatsim.core.position.frame import Frames
from nanosatsim.core.state.spacecraft import SpacecraftState


from typing import List

from nanosatsim.core.vector import Vector

""""""


class MagneticForce(ForceModel):
    """
    Here we implement a magnetic force model which will calculate the forces which the
    satillite will experience due to the earths magnetic field and the magnetoquers.
    """

    def __init__(self) -> None:
        super().__init__()

    """
    @staticmethod
    def get_magnetic_field_vector_ned(date: AbsoluteDate, lla_position: GeodeticPoint) -> Vector:
        year = GeoMagneticFieldProvider.getDecimalYear(date
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
    """

    # def acceleration(self, s: SpacecraftState, array: List[float]) -> Vector:
    """
        tau = mu X B

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
            moment = Vector(moment_tmp[0], moment_tmp[1], moment_tmp[2])
        else:
            moment = Vector(0.0, 0.0, 0.0)

        return Vector.crossProduct(
            moment,
            MagneticForce.get_magnetic_field_vector_ned(date, satLatLonAlt))
        """
