from skeletons.actions import Action
from skeletons.states import State


class ProblemNode:
    def __init__(self, prev_state, state, actions):
        self.prev_state = prev_state
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
    def __init__(self, initial_state, goal_states, step_cost):
        """

        :param initial_state: description of the initial state
        :param goal_states: set of states that would satisfy the goal
        :param step_cost:
                function(s1, a, s2=None):
                    :param s1: initial state
                    :param a: action applied to s1
                    :param s2: optional resulting state. (is the mapping of action(s) one to one? if not then this is required)
                    :return: numeric
        """
        self.initial_state = initial_state
        self.goal_states = goal_states
        self.step_cost = step_cost
        self.state_space_head = self.generate_state_space()

    def path_cost(self, path):
        """
        :param path: [(state1, action1), ... , (state_n: action_n)]
        :return: numeric
        """
        return sum(list(map(lambda t: self.step_cost(t[0], t[1]), path)))



    def test(self, state):
        if State.is_in(state, self.goal_states):
            return True
        return False





