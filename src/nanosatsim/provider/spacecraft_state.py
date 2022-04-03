from org.orekit.propagation import SpacecraftState as _SpacecraftState
from org.orekit.propagation import PythonAdditionalStateProvider as _PythonAdditionalStateProvider  # type: ignore


class SpacecraftState(_SpacecraftState):
    pass


class AdditionalStateProvider(_PythonAdditionalStateProvider):
    pass
