import numpy as np


class Space:
    def __init__(self):
        self.name = None


class Grid2D(Space):
    def __init__(self, columns, rows):
        self.name = 'Grid'
        self.c = columns
        self.r = rows
        self.grid = np.zeros(shape=(rows, columns))

    def __repr__(self):
        return self.__class__.__name__

    def __eq__(self, other):
        return repr(self) == other


