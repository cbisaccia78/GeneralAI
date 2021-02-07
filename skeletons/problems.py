from actions import Action


class ProblemNode:
    def __init__(self, state):
        self.state = state
        self.actions = []
        return


class ProblemEdge:
    def __init__(self):
        return


class Problem:
    """
    Problem formulation is the process of deciding what actions
    and states to consider, given a goal.

    Problem formulation requires:
        - a description of the initial state ie) in(Arad)
        - a way to generate the valid actions in a particular state
            - actions(s) returns a set of actions executable in s
            - for example, actions(in(arad)) = {Go(Sibiu), Go(Timisoara ), Go(Zerind )}
        - a description of what each action does (transition model) specified by Result(a, s) where a and s are actions
            - this Result(a,s) function returns a state
        - a state space description - Together, the initial state, actions, and transition model implicitly define the
        state space of the problem— the set of all states reachable from the initial state by any sequence
        of actions. The state space forms a directed network or graph in which the nodes
        are states and the links between nodes are actions.
        -
    """
    def __init__(self, initial_state, goal):
        self.initial_state = initial_state
        self.goal = goal
        self.state_space = self.generate_state_space()
        self.head = None

    def actions(self, state):
        return

    def generate_state_space(self, depth=-1):
        # uses initial_state
        self.head = ProblemNode(self.initial_state)

        return []



