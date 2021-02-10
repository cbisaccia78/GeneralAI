from skeletons.environments import GridEnv2D
from skeletons.agents import BasicProblemSolver
from skeletons.helpers import manhattan
import numpy as np
from skeletons.things import Thing
from skeletons.states import State
col = 10
row = 10
num_agents = 1


def init_world():
    world = GridEnv2D(name='Vacuum World', col=col, row=row)
    agents = [BasicProblemSolver(
        name=('solver' + str(i)),
        environment=world,
        goal_states=[np.zeros((col, row))],
        step_cost=manhattan) for i in range(0, num_agents)]
    agents[0].agent_program()


def test_state():
    state1 = State(things=[Thing('int1', np.zeros((3, 4))), Thing('int2', np.zeros((3, 4)))])
    state2 = State(things=[Thing('int1', np.zeros((3, 4))), Thing('int2', np.zeros((3, 4)))])
    print(state1 == state2)



print('test')
test_state()
