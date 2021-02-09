from skeletons.spaces import Grid2D
from skeletons.agents import BasicProblemSolver
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

    def assign_state(self, agent):
        # determine the local state of the particular agent in the environment
        return

    def assign_local(self, agent):
        return


class GridEnv2D(Environment):
    def __init__(self, col, row, num_agents=0, agents=None, allowed_agents=None):
        self.allowed_agents=allowed_agents
        self.agents = agents if agents and self.agent_test(agents) else agents
        self.num_agents=num_agents
        self.space = Grid2D(columns=col, rows=row)
        self.rules = []

    def assign_location(self, agent):
        # find empty x loc
        for x in self.space.grid[0]:
            return

    def agent_test(self, agents):
        if not self.allowed_agents:
            return True

        if isinstance(agents, list):
            for agent in agents:
                if repr(agent) not in self.allowed_agents:
                    raise Exception()
            return True

        if repr(agents) in self.allowed_agents:
            return True

        raise Exception()


class VacuumWorld(GridEnv2D):
    def __init__(self, col, row, num_agents=0, agents=None):
        super().__init__(col, row, num_agents, agents)
        self.world = [np.arange(self.space.c*self.space.r).reshape(self.space.r, self.space.c)]
        self.allowed_agents = {"Vacuum": self.space.c + self.space.r}
        self.agents = {"Vacuum": []}

    def add_agent(self, name=None):
        num_agents = len(self.agents)
        if len(num_agents) >= self.space.c + self.space.r:
            raise ValueError('too many agents')
        self.agents['Vacuum'] += BasicProblemSolver(name=(name if name else 'Vacuum ' + str(num_agents) + '1'), )
        return



