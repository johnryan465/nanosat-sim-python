from typing import List
from nanosatsim.core.sensor import Sensor
from nanosatsim.core.state.spacecraft import SpacecraftState


class Magnetometer(Sensor):
    def get_name(self) -> str:
        return "magnetometer"

    def get_new_state(self, state: SpacecraftState) -> List[float]:
        """
        This calculates the sensor values

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
        """
        return [0.0, 0.0]
