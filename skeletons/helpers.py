from skeletons.states import State
from skeletons.actions import Action


def manhattan(s1: State, a: Action, s2: State = None):
    loc1 = s1.location
    loc2 = s2.location
    return loc2.x - loc1.x + loc2.y - loc1.y


def basic_eval(state):
    return state.location


"""
________________________________________________________________________________________________________________________
Goal Functions
"""





