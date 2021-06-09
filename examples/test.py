from skeletons.environments import VacuumWorld
from skeletons.agents import BasicProblemSolver
from skeletons.helpers import manhattan
from skeletons.actuators import Mover
from skeletons.sensors import VacuumSensor
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
        goal_states=[np.zeros((col, row))],
        actuators=[Mover()],
        sensors=[VacuumSensor],
        step_cost=manhattan) for i in range(0, num_agents)]
    world.start_agents()


init_world()
