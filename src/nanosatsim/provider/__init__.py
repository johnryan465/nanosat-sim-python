from abc import ABC, abstractmethod

from nanosatsim.provider.constants import Constants


class Provider(ABC):
    """
    Base class for all providers.
    """
    @property
    @abstractmethod
    def constants(self) -> Constants:
        pass
