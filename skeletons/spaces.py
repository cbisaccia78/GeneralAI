import numpy as np


class Space:
    def __init__(self):
        self.name = None


class Grid2D(Space):
    def __init__(self, columns, rows, grid=None):
        self.c = columns
        self.r = rows
        self.grid = grid if isinstance(grid, np.ndarray) else np.full(shape=(rows, columns), fill_value=0.5)

    def __repr__(self):
        return Grid2D.__name__

    def __eq__(self, other):
        return repr(self) == other


