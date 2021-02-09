from skeletons.problems import Problem
from skeletons.sensors import VacuumSensor


class Agent:
    def __init__(self, name=None, environment=None):
        self.name = name
        self.sensors = None
        self.percept_history = []
        self.actuators = None
        self.environment = environment
        self.state, self.local_env = self.notify_env()

    def __repr__(self):
        return self.__class__.__name__

    def update_state(self, percepts):
        self.percept_history.extend(percepts)
        self.local_env.update_state(percepts)

    def notify_env(self):
        if self.environment:
            self.environment.agents[repr(self)].append(self)
            return self.environment.assign_state(self), self.environment.assign_local(self)

    def sense(self):
        precepts = []
        for sensor in self.sensors:
            precepts.append(sensor.precepts)
        return precepts


class BasicProblemSolver(Agent):
    """
    Searches sequentially at each layer for a solution to specified problem in particular environment
    """
    def __init__(self, environment=None, name=None,  closed_loop=True, problem=None):
        super(BasicProblemSolver, self).__init__(name, environment)
        self.closed_loop = closed_loop  # AKA: self.eyes_open = eyes_open
        self.problem = problem if problem else Problem()

    def search(self, problem):
        """
        :param problem: provides filtering of environment into a relevant set of features (state space),
        coupled with a path cost function, a goal evaluation function, and much much more!
        :return: sequence of actions that define a solution
        """
        seq = []
        head = problem.state_space_head
        ptr = head.actions.pop()
        while (not problem.test(ptr.state)) and True:
            return
        return seq[0] if self.closed_loop else seq

    def agent_program(self):
        while not self.problem.test(self.state):
            precepts = self.sense()
            self.act(precepts)
        return True

    def act(self, percepts):
        self.update_state(percepts)
        actions = self.search(self.problem)
        for action in actions:
            self.actuators[action.actuator_name].act(action)


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








