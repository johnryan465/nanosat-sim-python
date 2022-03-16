from org.orekit.propagation import PythonAdditionalStateProvider  # type: ignore

class SatelliteUpdaterStateProvider(PythonAdditionalStateProvider):
    def getName(self) -> str:
        return "sat"