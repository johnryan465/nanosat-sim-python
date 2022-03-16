from org.orekit.propagation import PythonAdditionalStateProvider  # type: ignore

class MagnetometerStateProvider(PythonAdditionalStateProvider):
    def getName(self) -> str:
        return "magnet"
