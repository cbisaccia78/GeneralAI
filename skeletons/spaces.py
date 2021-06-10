import numpy as np


class Space:
    def __init__(self):
        self.name = None


class Grid2D(Space):
    def __init__(self, columns, rows, initial=None):
        self.c = columns
        self.r = rows
        self.grid = np.full(shape=(rows, columns), fill_value=0.5) if initial is None else initial

    def __repr__(self):
        return Grid2D.__name__

    def __eq__(self, other):
        return repr(self) == repr(other) and np.array_equal(self.grid, other.grid)


