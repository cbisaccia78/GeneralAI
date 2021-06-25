from copy import deepcopy

from skeletons.states import State
from skeletons.actions import Action


"""
HELPER FUNCTIONS
___________________________________________________________
"""


def is_cycle(node, diameter):
    temp = node.parent
    count = 0
    while (count < diameter) and temp:
        if temp == node:
            return True
        count += 1
        temp = temp.parent
    return False


"""
EVAL FUNCTIONS
____________________________________________________________
"""


def manhattan(s1: State, a: Action, s2: State = None):
    loc1 = s1.location
    loc2 = s2.location
    return abs(loc2[0] - loc1[0]) + abs(loc2[1] - loc1[1])


def basic_eval(node):
    count = 0
    while node.parent:
        node = node.parent
        count += 1
    return count


def path_cost(node):
    return node.path_cost


def depth_cost(node, factor=-1):
    return factor * node.depth


"""
________________________________________________________________________________________________________________________
Goal Functions
"""





