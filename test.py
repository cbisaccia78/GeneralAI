from skeletons.environments import GridEnv2D
from skeletons.agents import BasicProblemSolver
from skeletons.helpers import manhattan
from skeletons.problems import Problem

col = 10
row = 10
num_agents = 1

world = GridEnv2D(name='Treasure Hunt', col=col, row=row)
agents = [BasicProblemSolver(name=('solver' + str(i)), environment=world, step_cost=manhattan) for i in range(0, num_agents)]
world.add_agents(agents)

