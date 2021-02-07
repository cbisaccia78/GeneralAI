class State:
    """
    a state should be relevant to a problem, as to not blow up the memory of the program by including
    extraneous information. for example, if the state is instantiated with a DriveToLocation problem,
    it will include info relevant to driving, but it wont include the current stock price of google.
    In this way the state is a subset or subclass of the current environment.
    """
    def __init__(self):
        return

    @staticmethod
    def sub_state(state1, state2):
        for attribute in state1.__dict__:
            if not hasattr(state2, attribute) or not getattr(state1, attribute).equals(state2.attribute):
                return False
        return True

    @staticmethod
    def are_equal(state1, state2):
        if not (State.sub_state(state1, state2) and State.sub_state(state2, state1)):
            return False
        return True

    @staticmethod
    def is_in(state1, states):
        for state in states:
            if State.sub_state(state1, state):
                return True
        return False
