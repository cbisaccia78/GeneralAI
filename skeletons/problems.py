from actions import Action
from skeletons.states import State


class ProblemNode:
    def __init__(self, state, actions):
        self.state = state
        self.actions = actions


class Problem:
    """
    Problem formulation is the process of deciding what actions
    and states to consider, given a goal.

    Problem formulation requires:
        - a description of the initial state ie) location of hand
        - a way to generate the valid actions in a particular state
            - actions(s) returns a set of actions executable in s
            - for example, actions(hand) = {Go(Sibiu), Go(Timisoara ), Go(Zerind )}
        - a description of what each action does (transition model) specified by Result(a, s) where a and s are actions
            - this Result(a,s) function returns a state
        - a state space description - Together, the initial state, actions, and transition model implicitly define the
        state space of the problem— the set of all states reachable from the initial state by any sequence
        of actions. The state space forms a directed network or graph in which the nodes
        are states and the links between nodes are actions.
        -
    """
    def __init__(self, initial_state, goal_states):
        self.initial_state = initial_state
        self.goal_states = goal_states
        self.state_space = self.generate_state_space()
        self.head = None

    def actions(self, state):
        return # list of actions executable from the current state

    def result(self, state, action):
        new_state = []
        return new_state

    def test(self, state):
        if State.is_in(state, self.goal_states):
            return True
        return False

    def generate_state_space(self, depth=-1):
        # uses initial_state
        self.head = ProblemNode(self.initial_state, self.actions(self.initial_state))

        return []



