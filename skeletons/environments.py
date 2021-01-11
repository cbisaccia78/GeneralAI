from spaces import Grid


class Environment:
    def __init__(self, agents):
        self.agents = agents
        self.space = None
        self.rules = None


class VacuumWorld(Environment):
    def __init__(self, agents):
        super().__init__(agents)
        self.space = Grid(columns=2, rows=1)

