from org.orekit.propagation import PythonAdditionalStateProvider

class SatelliteUpdaterStateProvider(PythonAdditionalStateProvider):
    def getName(self) -> str:
        return "sat"