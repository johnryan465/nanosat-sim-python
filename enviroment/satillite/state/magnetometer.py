from org.orekit.propagation import PythonAdditionalStateProvider

class MagnetometerStateProvider(PythonAdditionalStateProvider):
    def getName(self) -> str:
        return "magnet"
