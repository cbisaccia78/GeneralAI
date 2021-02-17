import numpy as np


class Space:
    def __init__(self):
        self.name = None


class Grid2D(Space):
    def __init__(self, columns, rows):
        self.c = columns
        self.r = rows
        self.grid = np.empty(shape=(rows, columns))

    def __repr__(self):
        return Grid2D.__name__

    def __eq__(self, other):
        return repr(self) == other


