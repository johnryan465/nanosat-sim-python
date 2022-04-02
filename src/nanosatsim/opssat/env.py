from typing import Iterable

import numpy as np
from nanosatsim.opssat.forcemodels.magnet import MagneticForce
from nanosatsim.simulator.enviroment import SpaceEnviroment
from numpy.typing import NDArray
from org.orekit.attitudes import Attitude
from org.orekit.bodies import OneAxisEllipsoid
from org.orekit.forces import (AbstractForceModel, ForceModel,
                               PythonForceModel)  # type: ignore
from org.orekit.forces.gravity import HolmesFeatherstoneAttractionModel
from org.orekit.forces.gravity.potential import GravityFieldFactory
from org.orekit.frames import FactoryManagedFrame, FramesFactory
from org.orekit.propagation.numerical import NumericalPropagator
from org.orekit.utils import Constants, IERSConventions


class OPSSATEnv(SpaceEnviroment):
    def get_force_models(self) -> Iterable[PythonForceModel]:
        itrf = FramesFactory.getITRF(IERSConventions.IERS_2010, True)
        gravity_provider = GravityFieldFactory.getNormalizedProvider(8, 8)
        gravity_force_model = HolmesFeatherstoneAttractionModel(itrf, gravity_provider)
        magnetic_force_model = MagneticForce()
        return [gravity_force_model, magnetic_force_model]

    def get_base_frame(self) -> FactoryManagedFrame:
        return FramesFactory.getITRF(IERSConventions.IERS_2010, True)
