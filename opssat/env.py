from typing import Iterable
from simulator.enviroment import Enviroment

import numpy as np
from numpy.typing import NDArray


from org.orekit.attitudes import Attitude
from org.orekit.bodies import OneAxisEllipsoid
from org.orekit.forces.gravity import HolmesFeatherstoneAttractionModel
from org.orekit.forces.gravity.potential import GravityFieldFactory
from org.orekit.frames import FramesFactory
from org.orekit.propagation.numerical import NumericalPropagator
from org.orekit.utils import IERSConventions
from simulator.enviroment import Enviroment
from org.orekit.utils import Constants



from org.orekit.forces import PythonForceModel, AbstractForceModel, ForceModel  # type: ignore


class OPSSATEnv(Enviroment):
    def get_force_models(self) -> Iterable[PythonForceModel]:
        itrf = FramesFactory.getITRF(IERSConventions.IERS_2010, True)
        gravityProvider = GravityFieldFactory.getNormalizedProvider(8, 8)
        gravityForceModel = HolmesFeatherstoneAttractionModel(itrf, gravityProvider)
        return [gravityForceModel]
