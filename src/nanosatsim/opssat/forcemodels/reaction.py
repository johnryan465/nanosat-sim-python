from datetime import datetime
from nanosatsim.provider.vector import Vector
from nanosatsim.provider.time import AbsoluteDate
from nanosatsim.provider.spacecraft_state import SpacecraftState
from nanosatsim.provider.frame import Frames
from nanosatsim.provider.force_model import ForceModel
from nanosatsim.provider.ellipsoid import OneAxisEllipsoid
from nanosatsim.provider.constants import Constants
from typing import List
from nanosatsim.provider.equations import TimeDerivativesEquations


class ReactionWheelForce(ForceModel):
    """
    Here we implement a force model for the reaction wheels


    """

    def __init__(self) -> None:
        super().__init__()

    def init(self, spacecraftState: SpacecraftState, absoluteDate: AbsoluteDate) -> None:
        pass

    def addContribution(
            self, spacecraftState: SpacecraftState, timeDerivativesEquations: TimeDerivativesEquations) -> None:
        a = self.acceleration(spacecraftState, self.getParameters())
        timeDerivativesEquations.addNonKeplerianAcceleration(a)

    def acceleration(self, s: SpacecraftState, array: List[float]) -> Vector:
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
            moment = Vector(moment_tmp[0], moment_tmp[1], moment_tmp[2])
        else:
            moment = Vector(0.0, 0.0, 0.0)

        return Vector.crossProduct(
            moment,
            self.get_magnetic_field_vector_ned(date, satLatLonAlt))
