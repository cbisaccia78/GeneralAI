
class Sensor:
    def __init__(self, name=None, default=None, agent=None):
        self.state = default
        self.name = name
        self.agent=agent


class VacuumSensor(Sensor):

    def sense(self):
        if 'dirty' in self.agent.curr_state_node.state.__dict__:
            return self.agent.curr_state_node.state.dirty



