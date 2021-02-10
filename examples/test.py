from skeletons.environments import GridEnv2D
from skeletons.agents import BasicProblemSolver
from skeletons.helpers import manhattan
import numpy as np
np.array_equal
col = 10
row = 10
num_agents = 1

world = GridEnv2D(name='Vacuum World', col=col, row=row)
agents = [BasicProblemSolver(name=('solver' + str(i)), environment=world, goal_states=[np.zeros((col, row))], step_cost=manhattan) for i in range(0, num_agents)]
agents[0].agent_program()

