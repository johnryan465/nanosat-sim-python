from typing import Iterable

from nanosatsim.core.force.magnet import GeoMagneticField
from nanosatsim.core.force import ForceModel
from nanosatsim.core.position.frame import Frame, Frames
from nanosatsim.core.force.gravity import HolmesFeatherstoneAttractionModel
from nanosatsim.core.enviroment import SpaceEnviroment


class OPSSATEnv(SpaceEnviroment):
    def get_force_models(self) -> Iterable[ForceModel]:
        gravity_force_model = HolmesFeatherstoneAttractionModel()
        magnetic_force_model = GeoMagneticField()
        return [gravity_force_model, magnetic_force_model]

    def get_base_frame(self) -> Frame:
        return Frames().getITRF()
