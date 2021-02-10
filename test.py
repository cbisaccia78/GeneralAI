from skeletons.environments import GridEnv2D
from skeletons.agents import BasicProblemSolver
from skeletons.problems import Problem

col = 10
row = 10
num_agents = int(col+row/10)

world = GridEnv2D(name='Vacuum World', col=col, row=row, )
agents = [BasicProblemSolver(name=('solver' + str(i)), environment=world, problem=Problem()) for i in range(0, num_agents)]
world.add_agents(agents)

