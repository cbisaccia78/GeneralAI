from skeletons.problems import Problem
from skeletons.states import StateNode
from skeletons.sensors import Sensor, VacuumSensor



class Agent:
    def __init__(self, name=None, environment=None):
        self.name = name
        self.sensors = None
        self.percept_history = []
        self.actuators = None
        self.environment = environment
        self.state, self.local_env = self.notify_env()
        self.ss_head = None

    def __repr__(self):
        return self.__class__.__name__

    def update_local_env(self, percepts):
        self.percept_history.extend(percepts)
        self.local_env.update_state(percepts)

    def notify_env(self):
        if self.environment:
            self.environment.add_agents(self)
            return self.environment.assign_initial_state(self), self.environment.assign_initial_local(self)

    def sense(self):
        precepts = []
        for sensor in self.sensors:
            precepts.append(sensor.precepts)
        return precepts


class BasicProblemSolver(Agent):
    """
    Searches sequentially at each layer for a solution to specified problem in particular environment
    """
    def __init__(self, environment=None, name=None,  closed_loop=True, goal_states=None, step_cost=None):
        super(BasicProblemSolver, self).__init__(name, environment)
        self.closed_loop = closed_loop  # AKA: self.eyes_open = eyes_open
        self.problem = Problem(initial_state=self.state, goal_states=goal_states, step_cost=step_cost)

    def actions(self, state):
        return []

    def _generate_state_space(self, node, depth, depth_limit):
        if depth == depth_limit:
            return
        node.gen_future_states(actions=self.actions(self.initial_state), actuators=self.actuators)
        if not node.future_state_nodes:
            return
        for future_node in node.future_state_nodes:
            self._generate_state_space(future_node)
        """
        :param head:
        :param depth:
        :return:
        """
        return

    def generate_state_space(self, depth=-1, starter=None):
        """
        num_states = sum_i(sum_j(thing_ij * num_values_thing_ij*)) for j ranging over all things in state i
        :param depth: specifies how deep the state space tree will go. -1 for exhaustion
        :return:
        """
        self.ss_head = self._generate_state_space(starter if starter else StateNode(prev_state=None, state=self.initial_state), depth)

    def search(self):
        """
        :makes use of self.problem: provides filtering of environment into a relevant set of features (state space),
        coupled with a path cost function, a goal evaluation function, and much much more!
        :returns: sequence of actions that define a solution
        """
        seq = []
        head = self.problem.state_space_head
        ptr = head.actions.pop()
        while (not self.problem.test(ptr.state)) and True:
            return
        return seq[0] if self.closed_loop else seq

    def agent_program(self):
        """
        Once the agent is instantiated this method can be called.
        Once called, it goes through a loop of sense -> act -> update -> goal_test
        """
        while not self.problem.test(self.state):
            precepts = self.sense()
            self.act(precepts)
        return True

    def act(self, percepts):
        """
        add the percepts to the agents history,
        then search the state space for action(s) which will satisfy goal
        after actions found, pass each action to its respective actuator
        :param percepts:
        :return:
        """
        self.update_state(percepts)
        actions = self.search()
        for action in actions:
            self.state = self.actuators[action.actuator_name].act(action, self.state)


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








