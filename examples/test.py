import sys

from skeletons.environments import VacuumWorld, PokerTable
from skeletons.agents import BasicProblemSolver
from skeletons.helpers import manhattan
from skeletons.actuators import Mover, Sucker
from skeletons.sensors import VacuumSensor
from skeletons.spaces import Grid2D
from skeletons.states import State
import numpy as np

col = 3
row = 3
num_agents = 1


def init_vaccum_world():
    world = VacuumWorld(name='Vacuum World', col=col, row=row)
    world.randomize_grid()
    agents = [BasicProblemSolver(
        name=('solver' + str(i)),
        environment=world,
        goal_states=[State(grid2d=Grid2D(col, row, grid=np.zeros((row, col))))],
        closed_loop=False,
        actuators=[Mover(), Sucker()],
        sensors=[VacuumSensor],
        step_cost=manhattan) for i in range(0, num_agents)]
    world.start_agents()
    world = None

def init_poker_world():
    world = PokerTable()
    agents = [PokerPlayer(
        name=('solver' + str(i)),
        environment=world,
        goal_states=[State(grid2d=Grid2D(col, row, grid=np.zeros((row, col))))],
        closed_loop=False,
        actuators=[Mover(), Sucker()],
        sensors=[VacuumSensor],
        step_cost=manhattan) for i in range(0, num_agents)]
    world.start_agents()
    world = None


"""with open('stats.txt', 'a+') as _file:
    for s in range(1,4):
        _file.write(f"({s}x{s})")
        col = s
        row = s
        big_guy = ""
        for i in range(0, 500):
            big_guy += init_world()
        _file.write(big_guy)
        _file.write("\n")
_file.close()"""
init_poker_world()
