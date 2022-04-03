import itertools
from typing import List, Tuple, Union
from gym import Env
from gym.spaces import Box
from nanosatsim.simulator.main import Simulator
from nanosatsim.opssat.sat import OPSSAT
from nanosatsim.opssat.env import OPSSATEnv
from nanosatsim.state import AccelerationValue, MagnetometerValue, MagnetorquerValue, MetresValue, RadiansValue, ReactionWheelValue, SatActionSpace, SatObservationSpace, SensorValue
from org.orekit.propagation import SpacecraftState
from org.orekit.bodies import OneAxisEllipsoid
from org.orekit.utils import Constants
from org.orekit.frames import FramesFactory
from org.orekit.utils import IERSConventions
from org.orekit.bodies import GeodeticPoint, FieldGeodeticPoint

from org.hipparchus.geometry.euclidean.threed import Vector3D
from org.orekit.frames import FramesFactory
from org.orekit.orbits import KeplerianOrbit
from org.orekit.time import AbsoluteDate, TimeScalesFactory
from org.orekit.utils import Constants, PVCoordinates


import pandas as pd
import plotly.express as px

import torch


class NanosatEnv(Env[torch.Tensor, torch.Tensor]):
    """
    This class uses Orekit to create an environment to propagate a satellite

    This wrapper should mean that uses of the enviroment should not have to deal with the JVM at all
    """

    def __init__(self) -> None:
        super().__init__()

        start_date = AbsoluteDate(2014, 1, 1, 23, 30, 00.000, TimeScalesFactory.getUTC())
        position = Vector3D(-6142438.668, 3492467.560, -25767.25680)
        velocity = Vector3D(505.8479685, 942.7809215, 7435.922231)
        init_orbit = KeplerianOrbit(PVCoordinates(position, velocity),
                                    FramesFactory.getEME2000(), start_date,
                                    Constants.EIGEN5C_EARTH_MU)
        satillite = OPSSAT(
            init_orbit
        )

        space_env = OPSSATEnv()

        self.simulator = Simulator(
            satillite,
            init_orbit,
            space_env,
            0.01
        )
        self._action_space = SatActionSpace(
            reaction_wheel_x=ReactionWheelValue(0.0),
            reaction_wheel_y=ReactionWheelValue(0.0),
            reaction_wheel_z=ReactionWheelValue(0.0),
            magnetorquer_x=MagnetorquerValue(0.0),
            magnetorquer_y=MagnetorquerValue(0.0),
            magnetorquer_z=MagnetorquerValue(0.0)
        )

        self._observation_space = SatObservationSpace(
            latitude=RadiansValue(0.0),
            longitude=RadiansValue(0.0),
            altitude=MetresValue(0.0),
            mag_field_b=MagnetometerValue(0.0),
            mag_field_r=MagnetometerValue(0.0),
            accel_x=AccelerationValue(0.0),
            accel_Y=AccelerationValue(0.0),
            accel_Z=AccelerationValue(0.0)
        )

    @staticmethod
    def get_lat_long_attitude(state: SpacecraftState) -> FieldGeodeticPoint:
        date = state.getDate()
        ecf = FramesFactory.getITRF(IERSConventions.IERS_2010, True)
        earth = OneAxisEllipsoid(Constants.WGS84_EARTH_EQUATORIAL_RADIUS, Constants.WGS84_EARTH_FLATTENING, ecf)
        satLatLonAlt = earth.transform(state.getPVCoordinates().getPosition(), FramesFactory.getEME2000(), date)

        return satLatLonAlt

    @staticmethod
    def to_observation_space(state: SpacecraftState) -> SatObservationSpace:
        """
        Here we define a translation between the orekit state and our representation
        """

        satLatLongAtt = NanosatEnv.get_lat_long_attitude(state)

        latitude = RadiansValue(satLatLongAtt.getLatitude())
        longitude = RadiansValue(satLatLongAtt.getLongitude())
        altitude = MetresValue(satLatLongAtt.getAltitude())
        mag_field = state.getAdditionalState("magnetometer")

        mag_field_b = MagnetometerValue(mag_field[0])
        mag_field_r = MagnetometerValue(mag_field[1])

        accel = state.getPVCoordinates().getAcceleration()
        accel_x = AccelerationValue(accel.getX())
        accel_y = AccelerationValue(accel.getY())
        accel_z = AccelerationValue(accel.getZ())

        return SatObservationSpace(
            latitude=latitude,
            longitude=longitude,
            altitude=altitude,
            mag_field_b=mag_field_b,
            mag_field_r=mag_field_r,
            accel_x=accel_x,
            accel_Y=accel_y,
            accel_Z=accel_z
        )

    def render(self, mode="human"):
        print(self.simulator.satellite.state)

    def reset(self, *args, **kwargs) -> Union[torch.Tensor, tuple[torch.Tensor, dict]]:
        return self.to_observation_space(self.simulator.satellite.state).to_tensor()

    def step(self, action: torch.Tensor) -> Tuple[torch.Tensor, float, bool, dict]:
        prev_state = self.simulator.satellite.state
        modified_state = self.apply_action(prev_state, action)
        self.simulator.propagator.resetInitialState(modified_state)
        final_state, done = self.simulator.step()
        reward = self.nadir_reward(final_state)
        return (self.to_observation_space(final_state).to_tensor(), reward, done, {})

    def observable_state(self) -> torch.Tensor:
        return self.to_observation_space(self.simulator.satellite.state).to_tensor()

    @property
    def action_space(self) -> Box:
        """
        Action Space
        - Reaction Wheel x3 dim=0
        - Magnetorquer x3 dim=1
        - Use magnetorquer vs read magnetometer x1 dim=2

        """
        return self._action_space.bound()

    @property
    def observation_space(self):
        """
        Observation Space
        - GPS Position [Longitude, Latitude, Altitude]
        - GPS Velocity [Velocity X, Velocity Y, Velocity Z]
        - GPS Acceleration [Acceleration X, Accleration Y, Acceleration Z]
        - Magnetometer [B, R]
        """
        return self._observation_space.bound()

    @staticmethod
    def nadir_reward(state: SpacecraftState) -> float:
        # get_down facing vector
        # get vector pointing directly down
        # penalise cross product
        satInBodyFrame = refToBody.transformPosition(scRef.getPosition())

        gpSat = shape.transform(satInBodyFrame, state.getFrame(), scRef.getDate())

        gpNadir = GeodeticPoint(gpSat.getLatitude(), gpSat.getLongitude(), 0.0)

        pNadirBody = shape.transform(gpNadir)

        pNadirRef = refToBody.getInverse().transformPosition(pNadirBody)

        satPosition = state.getPVCoordinates().getPosition()

        return satPosition.dotProduct(pNadirRef)

    @staticmethod
    def apply_action(state: SpacecraftState, action: torch.Tensor) -> SpacecraftState:
        """
        Here we modify the orekit state to add the signals we send to the controls
        which the simulator will use to update.
        """
        return state
