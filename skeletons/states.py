
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

    @staticmethod
    def sub_state(state1, state2):
        for attribute in state1.__dict__:
            if not (hasattr(state2, attribute) and getattr(state1, attribute) == getattr(state2, attribute)):
                return False
        return True

    @staticmethod
    def is_in(state1, states, reverse=False):
        if reverse:
            for state in states:
                if State.sub_state(state, state1):
                    return True
        else:
            for state in states:
                if State.sub_state(state1, state):
                    return True
        return False


class StateNode:
    def __init__(self, parent, prev_action, state, path_cost=None):
        self.parent = parent
        self.prev_action = prev_action
        self.state = state
        self.path_cost = path_cost(parent.state, prev_action, state) if path_cost else 0



