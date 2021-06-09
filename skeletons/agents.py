from copy import deepcopy
from skeletons.actions import Left, Right, Up, Down, Suck
from skeletons.problems import Problem
from skeletons.spaces import Grid2D
from skeletons.states import StateNode
from skeletons.percepts import Percepts
from functools import cache

class Agent:
    def __init__(self, name=None, environment=None):
        self.name = name
        self.sensors = None
        self.percept_history = Percepts()
        self.actuators = None
        self.environment = environment
        self.curr_state_node = self.get_initial_state()
        self.ss_head = None

    def __repr__(self):
        return self.__class__.__name__

    def update_local_env(self, percepts):
        self.percept_history.extend(percepts)

    def get_initial_state(self):
        if self.environment:
            return self.environment.assign_initial_state(self)

    def get_local_env(self):
        if self.environment:
            return self.environment.assign_initial_local(self)

    def sense(self):
        """
        :return:
        """
        for sensor in self.sensors:
            self.percept_history[(self.curr_state_node.state.location, self.environment.time)] = sensor.sense()


class BasicProblemSolver(Agent):
    """
    Searches sequentially at each layer for a solution to specified problem in particular environment
    """
    def __init__(
            self, environment=None,
            name=None,
            closed_loop=True,
            goal_states=None,
            step_cost=None,
            actuators=None,
            sensors=None
    ):
        super(BasicProblemSolver, self).__init__(name, environment)
        self.actuators = actuators
        self.sensors = [sensor(agent=self) for sensor in sensors]
        self.closed_loop = closed_loop  # AKA: self.eyes_open = eyes_open
        self.problem = Problem(initial_state=self.curr_state_node.state, goal_states=goal_states, step_cost=step_cost)
        self.frontier = []
        self.reached = {}

    def actions(self, state):
        properties = [prop for prop in vars(state) if not prop.startswith(("__"))]
        action_list = []
        for prop in properties:
            if prop == "location":
                action_list.extend([Left(), Right(), Up(), Down()])
            if prop == 'dirty':
                action_list.extend([Suck()])
        return action_list

    def agent_program(self):
        """
        Once called, agent goes through a loop of sense <-> act <-> goal_test
        """
        while not self.problem.test(self.environment.world_state_so_far(self.curr_state_node)):
            self.sense()
            for k in self.percept_history:
                print(self.percept_history[k])
            self.act()
        return True

    def act(self):
        """
        add the percepts to the agents history,
        then search the state space for action(s) which will satisfy goal
        after actions found, pass each action to its respective actuator
        :param percepts:
        :return:
        """
        action = self.search()
        if action:
            self.curr_state_node = StateNode(
                parent=self.curr_state_node,
                prev_action=action,
                state=self.actuators[action.actuator_name].act(
                    action,
                    self.curr_state_node.state
                )
            )

    def best_first_search(self, initial_node, depth_limit):
        goal = self.problem.test(initial_node.state)
        if depth_limit == 0:
            return goal
        future_nodes = self.environment.gen_future_nodes(initial_node, self.actions(initial_node), self.actuators)
        self.frontier.extend(future_nodes)
        self.reached = {initial_node.state: initial_node}
        while len(self.frontier) > 0:
            node = self.frontier.pop()
            if self.problem.test(node.state):
                return node
            for child in self.expand(node):
                s = child.state
                if s not in self.reached or child.path_cost < self.reached[s].path_cost:
                    self.reached[s] = child
                    self.frontier.append(child)
        return None

    def expand(self, node):
        s = node.state
        fns = self.environment.gen_future_nodes(node, self.actions(s), self.actuators)
        for fn in fns:
            fn.path_cost = node.path_cost + self.problem.step_cost(node.state, fn.prev_action, fn.state)
        return fns


    def search(self, depth=None, search_type="best_first"):
        """
        makes use of self.problem: provides filtering of environment into a relevant set of features (state space),
        coupled with a path cost function, a goal evaluation function, and much much more!
        Can currently only search from the agents current state.
        :param depth: if depth == None then it searches the whole state space
        :param search_type: defaults to best first search
        :returns: sequence of actions that define a solution.
        """
        goal = self.problem.test(self.curr_state_node)
        if goal:
            return self.curr_state_node
        return self.best_first_search(self.curr_state_node, depth_limit=depth)


class BasicUtility(Agent):
    pass


class TableDrivenAgent(Agent):
    def __init__(self, name, environment):
        super().__init__(name=name, environment=environment)
        self.tabulator = {}

    def agent_program(self, percept):
        """
        In the context of the brain-arm-bottle example, the brain would be the implementation of the agent function.
        ie) it takes a percept sequence(memory) and maps it to a given action (electrical/chemical impulse sent to the body)
        :param percept:
        :return:
        """
        self.percept_history.append(percept)
        return self.tabulator[self.percept_history]








