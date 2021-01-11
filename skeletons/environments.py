from spaces import Grid


class Environment:
    def __init__(self, agents):
        self.agents = agents
        self.space = None
        self.rules = None


class VacuumWorld(Environment):
    def __init__(self, agents, col, row):
        self.agents = agents
        if len(agents) > col + row:
            return 'too many agents'
        self.space = Grid(columns=col, rows=row)
        self.rules = []

