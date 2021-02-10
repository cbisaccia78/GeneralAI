from skeletons.environments import GridEnv2D
from skeletons.agents import BasicProblemSolver
from skeletons.helpers import manhattan

col = 10
row = 10
num_agents = 1

world = GridEnv2D(name='Vacuum World', col=col, row=row)
agents = [BasicProblemSolver(name=('solver' + str(i)), environment=world, step_cost=manhattan) for i in range(0, num_agents)]
print('hello')

