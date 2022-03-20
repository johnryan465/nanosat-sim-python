from abc import ABC, abstractmethod
from typing import Generic, List, TypeVar


from org.orekit.propagation import PythonAdditionalStateProvider  # type: ignore

from nanosatsim.spacecraft.actions import ActuatorAction
from org.orekit.propagation import SpacecraftState

class ActuatorState(ABC):
    pass

State = TypeVar("State", bound=ActuatorState)
Action = TypeVar("Action", bound=ActuatorAction)


class Actuator(PythonAdditionalStateProvider, Generic[State, Action]):
    @property
    @abstractmethod
    def state(self) -> State:
        """
        Get the current state of the actuator
        """

    @state.setter
    @abstractmethod
    def state(self, state: State) -> None:
        """
        Set the current state of the actuator
        """

    @abstractmethod
    def actuate(self, action: Action) -> None:
        """
        This function performs the defined action, which will update states
        which will be interpreted by the force model
        """

    def getAdditionalState(self, state: SpacecraftState) ->  List[float]:
        """
        Returns an Orekit State Provider which represents what the sensor records
        """
        return self.get_new_state(state)

    @abstractmethod
    def get_new_state(self, state: SpacecraftState) -> List[float]:
        """
        This calculates the sensor values and sets the fields
        """

    def getName(self) -> str:
        """
        Return state provider names
        """
        return self.get_name()

    @abstractmethod
    def get_name(self) -> str:
        """
        Return state provider names
        """
