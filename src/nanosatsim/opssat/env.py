from typing import Iterable

from nanosatsim.opssat.forcemodels.magnet import MagneticForce
from nanosatsim.provider.force_model import ForceModel
from nanosatsim.provider.frame import Frame, Frames
from nanosatsim.provider.gravity import GravityFieldFactory, HolmesFeatherstoneAttractionModel
from nanosatsim.simulator.enviroment import Enviroment


class OPSSATEnv(Enviroment):
    def get_force_models(self) -> Iterable[ForceModel]:
        itrf = Frames().getITRF()
        gravity_provider = GravityFieldFactory.getNormalizedProvider(8, 8)
        gravity_force_model = HolmesFeatherstoneAttractionModel(itrf, gravity_provider)
        magnetic_force_model = MagneticForce()
        return [gravity_force_model, magnetic_force_model]

    def get_base_frame(self) -> Frame:
        return Frames().getITRF()
