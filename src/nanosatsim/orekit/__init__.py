from nanosatsim.orekit.constants import OrekitConstants
from nanosatsim.provider import Provider
from nanosatsim.provider.constants import Constants


class OrekitProvider(Provider):
    def __init__(self):
        self._constants = OrekitConstants()

    @property
    def constasts(self) -> Constants:
        return self._constants
