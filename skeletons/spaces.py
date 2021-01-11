import numpy as np


class Space:
    def __init__(self):
        self.name = None


class Grid(Space):
    def __init__(self, columns, rows):
        self.name = 'Grid'
        self.c = columns
        self.r = rows
        self.grid = np.random.default_rng().integers(1, size=(rows, columns))

