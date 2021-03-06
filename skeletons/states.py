from copy import copy, deepcopy
from types import FunctionType

from skeletons.actions import Action


class State:
    """
    a state should be relevant to a problem, as to not blow up the memory of the program by including
    extraneous information. for example, if the state is instantiated for a DriveToLocation problem,
    it will include info relevant to driving, but it wont include the current stock price of google.
    In this way the state is a subset or subclass of the current environment.
    """
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __eq__(self, other):
        return State.sub_state(self, other) and State.sub_state(other, self)

    def __hash__(self):
        return hash(self.__key())

    def __key(self):
        return (getattr(self, attr) for attr in self.__dict__)

    def properties(self):
        return self.__dict__

    @staticmethod
    def sub_state(state1, state2):
        for attribute in state1.__dict__:
            if not (hasattr(state2, attribute) and getattr(state1, attribute) == getattr(state2, attribute)):
                return False
        return True

    @staticmethod
    def is_in(state1, states):
        for state in states:
            if State.sub_state(state, state1):
                return True
        return False


class StateNode:
    def __init__(self, parent, prev_action, state, path_cost=None, depth=0):
        self.parent = parent
        self.depth = depth if isinstance(depth, int) else parent.depth + 1
        self.prev_action = prev_action
        self.state = state
        self.path_cost = (path_cost(parent.state, prev_action, state) if isinstance(path_cost, FunctionType) else path_cost) if path_cost else 0

    def __eq__(self, other):
        if not isinstance(other, StateNode):
            return False
        return self.depth == other.depth and self.prev_action == other.prev_action and self.state == other.state

    def __deepcopy__(self, memo):
        return StateNode(parent=self.parent, prev_action=self.prev_action, state=deepcopy(self.state, memo), path_cost=self.path_cost)



