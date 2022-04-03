from typing import List
from nanosatsim.provider.constants import Constants
from nanosatsim.provider.ellipsoid import OneAxisEllipsoid
from nanosatsim.provider.frame import Frames
from nanosatsim.provider.point import GeodeticPoint
from nanosatsim.provider.spacecraft_state import AdditionalStateProvider, SpacecraftState
from nanosatsim.opssat.forcemodels.magnet import MagneticForce


from nanosatsim.provider.spacecraft_state import SpacecraftState


class MagnetometerStateProvider(AdditionalStateProvider):
    def getName(self) -> str:
        return "magnetometer"

    def getAdditionalState(self, state: SpacecraftState) -> List[float]:
        """
        This calculates the sensor values
        """

        transform_eci_sat = state.toTransform()
        date = state.getDate()

        ecf = Frames().getITRF()
        earth = OneAxisEllipsoid(Constants.WGS84_EARTH_EQUATORIAL_RADIUS, Constants.WGS84_EARTH_FLATTENING, ecf)
        lla = earth.transform(state.getPVCoordinates().getPosition(), Frames().getEME2000(), date)

        field_ned = MagneticForce.get_magnetic_field_vector_ned(date, lla)

        # We convert to a Topo Frame
        field_topo = GeodeticPoint(field_ned.getY(),
                                   field_ned.getX(),
                                   -field_ned.getZ())

        # We then convert to ECF, ECI and then to the satillite

        # TopocentricFrame(earth, )

        return [0.0, 0.0]
