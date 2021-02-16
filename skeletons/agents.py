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
        self.curr_state_node = self.get_initial_state
        self.local_env = self.get_local_env() if self.curr_state_node else None
        self.ss_head = None

    def __repr__(self):
        return self.__class__.__name__

    def update_local_env(self, percepts):
        self.percept_history.extend(percepts)
        self.local_env.update_state(percepts)

    def get_initial_state(self):
        if self.environment:
            self.environment.add_agents(self)
            return self.environment.assign_initial_state(self)

    def get_local_env(self):
        if self.environment:
            return self.environment.assign_initial_local(self)

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
        self.problem = Problem(initial_state=self.curr_state_node.state, goal_states=goal_states, step_cost=step_cost)

    def actions(self, state):
        return []

    def _generate_state_space(self, node, depth, depth_limit):
        if depth_limit:
            if depth == depth_limit:
                return
        node.future_state_nodes = self.local_env.gen_future_states(state_node=node, actions=self.actions(self.curr_state_node.state), actuators=self.actuators)
        if not node.future_state_nodes:
            return
        for future_node in node.future_state_nodes:
            self._generate_state_space(future_node, depth=depth+1, depth_limit=depth_limit)
        """
        :param head:
        :param depth:
        :return:
        """
        return

    def generate_state_space(self, depth=None, starter=None):
        """
        num_states = sum_i(sum_j(thing_ij * num_values_thing_ij*)) for j ranging over all things in state i
        :param starter: initial node
        :param depth: specifies how deep the state space tree will go. None for exhaustion
        :return:
        """
        if starter:
            initial = starter
        else:
            self.ss_head = StateNode(prev_state_node=None, state=self.curr_state_node.state)
            initial = self.ss_head

        self._generate_state_space(initial, depth=0, depth_limit=depth)

    def agent_program(self):
        """
        Once the agent is instantiated this method can be called.
        Once called, it goes through a loop of sense -> act -> update -> goal_test
        """
        self.generate_state_space(starter=self.ss_head)
        self.curr_state_node = self.ss_head
        while not self.problem.test(self.curr_state_node.state):
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
        self.percept_history.append(percepts)
        action = self.search()
        if action:
            self.curr_state_node = StateNode(prev_state_node=self.curr_state_node, prev_action=action, state=self.actuators[action.actuator_name].act(action, self.curr_state_node.state))

    def _search(self, node, depth, depth_limit):
        goal = self.problem.test(node)
        if depth_limit:
            if depth == depth_limit:
                return node if goal else None
        if not node.future_state_nodes:
            return node if goal else None
        if goal:
            return node
        for fn in node.future_state_nodes:
            found = self._search(fn, depth=depth+1, depth_limit=depth_limit)
            if found:
                return found
        return None

    def search(self, depth=None):
        """
        makes use of self.problem: provides filtering of environment into a relevant set of features (state space),
        coupled with a path cost function, a goal evaluation function, and much much more!
        Can currently only search from the agents current state.
        :param depth: if depth == None then it searches the whole state space
        :returns: sequence of actions that define a solution
        """
        return self._search(self.curr_state_node, depth=0, depth_limit=depth)


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








