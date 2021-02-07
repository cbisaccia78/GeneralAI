from skeletons.sensors import VacuumSensor


class Agent:
    def __init__(self, name=None, environment=None):
        self.name = name
        self.sensors = None
        self.percept_history = []
        self.actuators = None
        self.environment = environment
        self.local_env = self.notify_env()

    def __repr__(self):
        return self.__class__.__name__

    def update_state(self, percepts):
        self.percept_history.extend(percepts)
        self.local_env.update_state(percepts)

    def notify_env(self):
        if self.environment:
            self.environment.agents[repr(self)].append(self)
            return self.environment.assign_partial(self)

    def sense(self):
        precepts = []
        for sensor in self.sensors:
            precepts.append(sensor.precepts)
        return precepts


class ProblemSolver(Agent):

    def __init__(self, problem, environment, name=None,  closed_loop=True):
        super(ProblemSolver, self).__init__(name, environment)
        self.closed_loop = closed_loop  # self.eyes_open = eyes_open
        self.problem = problem

    def search(self):
        seq = []
        return seq[0] if self.closed_loop else seq

    def agent_program(self):
        while not self.problem.goal.test(self.state):
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








