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
            self.percept_history[(self.curr_state_node.state.location.data, self.environment.time)] = sensor.sense()


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

    def actions(self, state):
        properties = [prop for prop in vars(state) if not prop.startswith(("__"))]
        action_list = []
        for prop in properties:
            if prop == "Location":
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
                prev_state_node=self.curr_state_node,
                prev_action=action,
                state=self.actuators[action.actuator_name].act(
                    action,
                    self.curr_state_node.state
                )
            )

    def _search(self, node, wssf, depth, depth_limit):
        goal = self.problem.test(wssf)
        if depth_limit:
            if depth == depth_limit:
                return node if goal else None
        if not node.future_state_nodes:
            return node if goal else None
        if goal:
            return node
        for fn in node.future_state_nodes:
            found = self._search(fn, self.environment.wssf_and_new(wssf, fn.state), depth=depth+1, depth_limit=depth_limit)
            if found:
                return found
        return None

    def search(self, depth=None):
        """
        makes use of self.problem: provides filtering of environment into a relevant set of features (state space),
        coupled with a path cost function, a goal evaluation function, and much much more!
        Can currently only search from the agents current state.
        :param depth: if depth == None then it searches the whole state space
        :returns: sequence of actions that define a solution.
        """
        return self._search(self.curr_state_node, self.environment.world_state_so_far(self.curr_state_node), depth=0, depth_limit=depth)


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








