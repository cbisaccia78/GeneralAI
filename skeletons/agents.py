from sensors import VacuumSensor


class Agent:
    def __init__(self, name=None, environment=None):
        self.name = name
        self.sensors = None
        self.percept_history = None
        self.actuators = None
        self.environment = environment

    def agent_function(self, percepts=None):
        return 'some action from some actuator based on given percepts/environment'


class Vacuum(Agent):
    def __init__(self):
        self.sensors = VacuumSensor()





