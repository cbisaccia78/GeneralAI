from skeletons.spaces import Grid2D
from skeletons.agents import Vacuum
import numpy as np


class Environment:
    def __init__(self, *args):
        self.allowed_agents = {}
        self.agents = {}
        self.space = None
        self.rules = None

    def step(self):
        return

    def start(self, steps=None):
        return


class GridEnv2D(Environment):
    def __init__(self, col, row):
        self.agents = {}
        self.space = Grid2D(columns=col, rows=row)
        self.rules = []

    def assign_loc(self, agent):
        # find empty x loc
        for x in self.space.grid[0]:
            return


class VacuumWorld(GridEnv2D):
    def __init__(self, col, row):
        super().__init__(col, row)
        self.world = [np.arange(self.space.c*self.space.r).reshape(self.space.r, self.space.c)]
        self.allowed_agents = {"Vacuum": self.space.c + self.space.r}
        self.agents = {"Vacuum": []}

    def add_agent(self, name=None):
        num_agents = len(self.agents)
        if len(num_agents) >= self.space.c + self.space.r:
            raise ValueError('too many agents')
        self.agents['vacuums'] += Vacuum(name=name if name else 'Vacuum ' + num_agents + 1)
        return



