from typing import Iterable

from nanosatsim.opssat.forcemodels.magnet import MagneticForce
from nanosatsim.core.force import ForceModel
from nanosatsim.core.position.frame import Frame, Frames
from nanosatsim.core.force.gravity import HolmesFeatherstoneAttractionModel
from nanosatsim.simulator.enviroment import SpaceEnviroment


class OPSSATEnv(SpaceEnviroment):
    def get_force_models(self) -> Iterable[ForceModel]:
        gravity_force_model = HolmesFeatherstoneAttractionModel()  # itrf, gravity_provider)
        magnetic_force_model = MagneticForce()
        return []  # [gravity_force_model]  # , magnetic_force_model]

    def get_base_frame(self) -> Frame:
        return Frames().getITRF()
