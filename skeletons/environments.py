from skeletons.spaces import Grid
from skeletons.agents import Vacuum


class Environment:
    def __init__(self, *args):
        self.agents = {}
        self.space = None
        self.rules = None


class VacuumWorld(Environment):
    def __init__(self, col, row):

        self.agents = {"vacuums": []}
        self.space = Grid(columns=col, rows=row)
        self.rules = []

    def add_agent(self, name=None):
        num_agents = len(self.agents)
        if len(num_agents) >= self.space.c + self.space.r:
            raise ValueError('too many agents')
        self.agents['vacuums'] += Vacuum(name=name if name else 'Vacuum ' + num_agents + 1)
        return
