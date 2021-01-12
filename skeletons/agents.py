from skeletons.sensors import VacuumSensor


class Agent:
    def __init__(self, name=None, environment=None):
        self.name = name
        self.sensors = None
        self.percept_history = None
        self.actuators = None
        self.environment = environment
        self.notify_env()

    def agent_function(self, *args):
        return

    def notify_env(self):
        self.environment.agents[self.name] += self


class Vacuum(Agent):
    def __init__(self, name, environment):
        super().__init__(name=name, environment=environment)
        self.sensors = VacuumSensor()
        self.actuators = []

    def suck(self):
        return





