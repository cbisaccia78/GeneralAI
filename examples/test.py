import sys

from skeletons.environments import VacuumWorld
from skeletons.agents import BasicProblemSolver
from skeletons.helpers import manhattan
from skeletons.actuators import Mover, Sucker
from skeletons.sensors import VacuumSensor
from skeletons.spaces import Grid2D
from skeletons.states import State
import numpy as np

col = 10
row = 10
num_agents = 1


def init_world():
    world = VacuumWorld(name='Vacuum World', col=col, row=row)
    world.randomize_grid()
    agents = [BasicProblemSolver(
        name=('solver' + str(i)),
        environment=world,
        goal_states=[State(grid2d=Grid2D(col, row, initial=np.zeros((col, row))))],
        closed_loop=False,
        actuators=[Mover(), Sucker()],
        sensors=[VacuumSensor],
        step_cost=manhattan) for i in range(0, num_agents)]
    world.start_agents()

sys.setrecursionlimit(10000000)
init_world()
