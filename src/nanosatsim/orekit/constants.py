from org.orekit.utils import Constants as _Constants

from nanosatsim.provider.constants import Constants


class OrekitConstants(Constants):
    @property
    def WGS84_EARTH_EQUATORIAL_RADIUS(self) -> float:
        return _Constants.WGS84_EARTH_EQUATORIAL_RADIUS

    @property
    def WGS84_EARTH_FLATTENING(self) -> float:
        return _Constants.WGS84_EARTH_FLATTENING

    @property
    def WGS84_EARTH_MU(self) -> float:
        return _Constants.WGS84_EARTH_MU
