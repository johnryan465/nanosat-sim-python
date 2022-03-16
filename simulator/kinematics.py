from numpy import array
from org.hipparchus.geometry.euclidean.threed import Rotation
from org.orekit.attitudes import PythonAttitudeProvider  # type: ignore
from org.orekit.attitudes import PythonAttitudeProviderModifier  # type: ignore
from org.orekit.attitudes import Attitude
from org.orekit.frames import Frame
from org.orekit.time import AbsoluteDate
from org.orekit.utils import (AngularCoordinates, PVCoordinatesProvider,
                              TimeStampedAngularCoordinates)
from pyquaternion import Quaternion
from spacecraft.satellite import Satellite


class Kinematics(PythonAttitudeProvider):
    """
    This class updates the rotation quarturnions
    """

    def __init__(self, attitude: Attitude, satellite: Satellite) -> None:
        self.previous_attitude = attitude
        self.satellite = satellite

    @property
    def previous_attitude(self) -> Attitude:
        return self._previous_attitude

    @previous_attitude.setter
    def previous_attitude(self, previous_attitude: Attitude) -> None:
        self._previous_attitude = previous_attitude

    def getAttitude(self, pvProv: PVCoordinatesProvider, date: AbsoluteDate, frame: Frame) -> Attitude:
        Δ = date.durationFrom(self.previous_attitude.getDate())

        if Δ <= 0:
            return self.previous_attitude.withReferenceFrame(frame)

        α = self.previous_attitude.getRotationAcceleration()
        ω = self.previous_attitude.getSpin()
        θ = self.previous_attitude.getRotation()
        # We perform first order approximation of the oretation from the derivative
        ω_q = Quaternion(imaginary=array([α.getX(), α.getY(), α.getZ()]))

        q = Quaternion(
            real=θ.getQ3(),
            imaginary=array([θ.getQ0(),
                             θ.getQ1(),
                             θ.getQ2()])
        )
        q̂ = q + (Δ * 0.5 * (ω_q * q))
        updated_rotation = Rotation(q̂[0], q̂[1], q̂[2], q̂[3], True)

        sac = AngularCoordinates(updated_rotation, ω, α)
        tsac = TimeStampedAngularCoordinates(
            date.shiftedBy(Δ),
            sac.getRotation(),
            sac.getRotationRate(),
            sac.getRotationAcceleration())
        shifted = Attitude(frame, tsac)

        self.previous_attitude = shifted

        return self.previous_attitude.withReferenceFrame(frame)
