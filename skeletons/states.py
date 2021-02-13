from skeletons.things import Thing


class State:
    """
    a state should be relevant to a problem, as to not blow up the memory of the program by including
    extraneous information. for example, if the state is instantiated for a DriveToLocation problem,
    it will include info relevant to driving, but it wont include the current stock price of google.
    In this way the state is a subset or subclass of the current environment.
    """
    def __init__(self, name=None, things=None):
        self.name = name
        for thing in things:
            setattr(self, thing.name, thing)

    def __eq__(self, other):
        if not (State.sub_state(self, other) and State.sub_state(other, self)):
            return False
        return True

    def generate_space(self):
        return

    @staticmethod
    def sub_state(state1, state2):
        for attribute in state1.__dict__:
            if not (hasattr(state2, attribute) and getattr(state1, attribute) == getattr(state2, attribute)):
                return False
        return True

    @staticmethod
    def is_in(state1, states):
        for state in states:
            if State.sub_state(state1, state):
                return True
        return False


class StateNode:
    def __init__(self, prev_state_node, prev_action, state):
        self.prev_state_node = prev_state_node
        self.prev_action = prev_action
        self.state = state
        self.future_state_nodes = []

    def gen_future_states(self, actions, actuators):
        for action in actions:
            valid_actuator = None
            for actuator in actuators:
                if action in actuator.actions:
                    valid_actuator = actuator
                    break
            if not valid_actuator:
                continue
            future_state = actuator.act(action)
            if future_state:
                self.future_state_nodes.append(StateNode(prev_state_node=self, prev_action=action, state=actuator.act(action)))
