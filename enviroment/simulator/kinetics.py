from org.orekit.attitudes import Attitude
from org.orekit.attitudes import AttitudeProvider
from org.orekit.attitudes import PythonAttitudeProviderModifier
from org.orekit.frames import Frame
from org.orekit.time import AbsoluteDate
from org.orekit.utils import PVCoordinatesProvider
from org.hipparchus.geometry.euclidean.threed import Vector3D
from org.hipparchus.random import RandomDataGenerator
from numpy import array
from enviroment.satillite.sensorsat import SensorSatellite
from enviroment.simulator.kinematics import Kinematics
from enviroment.utils.matrix import cross_product_matrix


class Kinetics(PythonAttitudeProviderModifier):

    def __init__(self, base_provider: Kinematics, satellite: SensorSatellite) -> None:
        if satellite is None:
            raise ValueError('Satellite must be defined')

        self.base_provider = base_provider
        self.satellite = satellite

        if self.satellite.get_external_torques_magnitude() != 0:
            self.external_torque_generator = RandomDataGenerator()
        else:
            self.external_torque_generator = None

    def getUnderlyingAttitudeProvider(self) -> AttitudeProvider:
        return self.base_provider

    def getAttitude(self, pvProv: PVCoordinatesProvider, date: AbsoluteDate, frame: Frame) -> Attitude:

        previous_attitude = self.base_provider.previous_attitude
        Δ = date.durationFrom(previous_attitude.getDate())

        if Δ <= 0:
            return previous_attitude

        ω = array(previous_attitude.getSpin().toArray())

        external_torque = array([0, 0, 0])
        if self.external_torque_generator is not None:
            external_torque = array([
                self.external_torque_generator.nextNormal(self.satellite.get_external_torques_magnitude(), 1.0),
                self.external_torque_generator.nextNormal(self.satellite.get_external_torques_magnitude(), 1.0),
                self.external_torque_generator.nextNormal(self.satellite.get_external_torques_magnitude(), 1.0)])

        ϵ_1 = array([0, 0, 0])
        if self.satellite.get_set_of_magnetorquers() is not None:
            ϵ_1 = self.satellite.get_I_inverse() @ (array(self.satellite.get_set_of_magnetorquers().state.get_control_torque()) + external_torque)

        ϵ_2 = (-1) * self.satellite.get_I_inverse() @ cross_product_matrix(ω) @ self.satellite.get_I() @ ω

        # reaction wheel
        ϵ_3 = array([0, 0, 0])
        ϵ_4 = array([0, 0, 0])
        if self.satellite.get_set_of_reaction_wheels() is None:
            ϵ_3 = -1 * self.satellite.get_I_inverse() @ cross_product_matrix(ω) @ array(
                self.satellite.get_set_of_reaction_wheels().state.get_angular_momentum(ω))
            ϵ_4 = -1 * self.satellite.get_I_inverse() @ array(self.satellite
                                                         .get_set_of_reaction_wheels().state
                                                         .get_control_torque())

        α = ϵ_1 + ϵ_2 + ϵ_3 + ϵ_4
        ω̂ = ω + (α * Δ)
        attitude_propagated_by_kinematics = self.getUnderlyingAttitudeProvider().getAttitude(pvProv, date, frame)

        # updating velocity using the results of kinetics propagation
        attitude_propagated_by_kinematics_and_kinetics = Attitude(
            date, frame, attitude_propagated_by_kinematics.getRotation(),
            Vector3D(ω̂[0], ω̂[1], ω̂[2]),
            Vector3D(α[0], α[1], α[2]))

        # updating for next propagation
        self.base_provider.previous_attitude = attitude_propagated_by_kinematics_and_kinetics
        return attitude_propagated_by_kinematics_and_kinetics
