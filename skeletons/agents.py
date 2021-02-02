from skeletons.sensors import VacuumSensor


class Agent:
    def __init__(self, name=None, environment=None):
        self.name = name
        self.sensors = None
        self.percept_history = None
        self.actuators = None
        self.environment = environment
        self.loc = self.notify_env()

    def __repr__(self):
        return self.__class__.__name__

    def agent_program(self, *args): # maps a given percept sequence to an action and sends action to actuators
        return

    def notify_env(self):
        if self.environment:
            self.environment.agents[repr(self)].append(self)
            return self.environment.assign_loc(self)


class TableDrivenAgent(Agent):
    def __init__(self, name, environment):
        super().__init__(name=name, environment=environment)
        self.percept_history = []
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


class Vacuum(TableDrivenAgent):
    def __init__(self, name, environment):
        super().__init__(name=name, environment=environment)
        self.sensors = VacuumSensor()
        self.actuators = []

    def suck(self):
        self.environment.space.grid[self.xloc][self.yloc] = 1
        return

    def left(self):
        self.xloc = self.xloc - 1

    def right(self):
        self.xloc = self.xloc + 1

    def up(self):
        self.yloc = self.yloc - 1

    def down(self):
        self.yloc = self.yloc +1





