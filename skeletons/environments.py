from skeletons.spaces import Grid2D
from skeletons.agents import BasicProblemSolver
import numpy as np


class Environment:
    def __init__(self, *args):
        self.allowed_agents = None
        self.agents = {}
        self.space = None
        self.rules = None

    def step(self):
        return

    def start(self, steps=None):
        return

    def add_agents(self, agents):
        if self.validate_agents(agents):
            for agent in agents:
                agent_name = repr(agent)
                if agent_name in self.agents:
                    self.agents[agent_name] += agent
                else:
                    self.agents[agent_name] = [agent]

    def validate_agents(self, agents):
        if not self.allowed_agents:
            raise Exception()

        if isinstance(agents, list):
            for agent in agents:
                if repr(agent) not in self.allowed_agents:
                    raise Exception()
            return True

        if repr(agents) in self.allowed_agents:
            return True

        raise Exception()

    def assign_initial_state(self, agent):
        # determine the local state of the particular agent in the environment, specific to agents particular problem
        return

    def assign_local_environment(self, agent):
        return


class GridEnv2D(Environment):
    def __init__(self, col, row, name=None):
        self.name = name
        self.allowed_agents = {'BasicProblemSolver': col + row}
        self.space = Grid2D(columns=col, rows=row)
        self.rules = []

    def assign_location(self, agent):
        # find empty x loc
        for x in self.space.grid[0]:
            return


class VacuumWorld(GridEnv2D):
    def __init__(self, col, row, num_agents=0, agents=None):
        super().__init__(col, row, num_agents, agents)
        self.world = [np.arange(col*row).reshape(row, col)]
        self.allowed_agents["Vacuum"] = col + row



