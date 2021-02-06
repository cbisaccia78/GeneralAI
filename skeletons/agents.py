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

    def agent_program(self, percept): # maps a given percept sequence to an action and sends action to actuators
        self.update_state(percept)
        return

    def update_state(self, percept):
        self.percept_history.append(percept)
        self.local_env.update_state(percept)

    def notify_env(self):
        if self.environment:
            self.environment.agents[repr(self)].append(self)
            return self.environment.assign_partial(self)


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


class ModelBasedReflexAgent(Agent):
    def __init__(self, name=None, environment=None):
        super(ModelBasedReflexAgent, self).__init__(name, environment)


class SimpleProblemSolvingAgent(Agent):
    def __init__(self, name, environment):
        super().__init__(name=name, environment=environment)
        self.seq = []

    def agent_program(self, percept):
        """
            state ← UPDATE-STATE (state, percept )
            if seq is empty then
                goal ← FORMULATE -GOAL (state)
                problem ← FORMULATE -PROBLEM (state, goal )
                seq ← SEARCH ( problem)
                if seq = failure then return a null action
            action ← FIRST (seq)
            seq ← REST (seq
            """
        self.update_state(percept)
        if not len(self.seq):
            goal = self.formulate_goal(state)
            problem = self.formulate_problem(state, goal)
            self.seq = self.search(problem)
            if not len(self.seq):
                return None
        return self.seq.pop(0)

    def search(self, problem):
        return []

    def formulate_goal(self, state):
        return True

    def formulate_problem(self, state, goal):
        return True




