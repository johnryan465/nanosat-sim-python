from abc import ABC, abstractmethod
from typing import Generic, List, TypeVar


from nanosatsim.core.controller.actions import Action as _Action
from nanosatsim.core.state.spacecraft import AdditionalStateProvider, SpacecraftState


class ActuatorState(ABC):
    pass


State = TypeVar("State", bound=ActuatorState)
Action = TypeVar("Action", bound=_Action)


class Actuator(AdditionalStateProvider, Generic[State, Action]):
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

    @abstractmethod
    def get_new_state(self, state: SpacecraftState) -> List[float]:
        """
        This calculates the sensor values and sets the fields
        """

    @abstractmethod
    def get_name(self) -> str:
        """
        Return state provider names
        """
