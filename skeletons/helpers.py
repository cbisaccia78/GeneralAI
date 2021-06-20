from skeletons.states import State
from skeletons.actions import Action


def manhattan(s1: State, a: Action, s2: State = None):
    loc1 = s1.location
    loc2 = s2.location
    return abs(loc2[0] - loc1[0]) + abs(loc2[1] - loc1[1])


def basic_eval(state):
    return state.location


"""
________________________________________________________________________________________________________________________
Goal Functions
"""





