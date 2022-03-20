from typing import List
from org.orekit.propagation import PythonAdditionalStateProvider, AdditionalStateProvider  # type: ignore
from org.orekit.propagation import SpacecraftState
from nanosatsim.opssat.forcemodels.magnet import MagneticForce


import org.orekit.utils
from org.orekit.propagation.events import EventDetector
from org.orekit.propagation import SpacecraftState
from org.orekit.forces import PythonForceModel, AbstractForceModel, ForceModel  # type: ignore
from org.orekit.propagation import SpacecraftState
from org.orekit.time import AbsoluteDate
from org.orekit.models.earth import GeoMagneticFieldFactory
from org.orekit.models.earth import GeoMagneticField
from org.orekit.time import TimeScalesFactory
from org.orekit.propagation.numerical import TimeDerivativesEquations
from numpy.typing import NDArray
from org.orekit.bodies import OneAxisEllipsoid
from org.orekit.frames import FramesFactory, TopocentricFrame
from org.orekit.utils import IERSConventions, Constants
from org.orekit.bodies import FieldGeodeticPoint, GeodeticPoint

from org.hipparchus.geometry.euclidean.threed import Vector3D
from nanosatsim.spacecraft.sensorsat import SensorSatellite


class MagnetometerStateProvider(PythonAdditionalStateProvider):
    def getName(self) -> str:
        return "measured_dipole_moment"

    def getAdditionalState(self, state: SpacecraftState) -> List[float]:
        """
        This calculates the sensor values
        """

        transform_eci_sat = state.toTransform()
        date = state.getDate()

        ecf = FramesFactory.getITRF(IERSConventions.IERS_2010, True)
        earth = OneAxisEllipsoid(Constants.WGS84_EARTH_EQUATORIAL_RADIUS, Constants.WGS84_EARTH_FLATTENING, ecf)
        lla = earth.transform(state.getPVCoordinates().getPosition(), FramesFactory.getEME2000(), date)

        field_ned = MagneticForce.get_magnetic_field_vector_ned(date, lla)

        # We convert to a Topo Frame
        field_topo = GeodeticPoint(field_ned.getY(),
                                   field_ned.getX(),
                                   -field_ned.getZ())

        # We then convert to ECF, ECI and then to the satillite

        # TopocentricFrame(earth, )

        return field_ned.toArray()
