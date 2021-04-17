
class Percepts(object):
    def __init__(self, max_time=-1, max_loc=None):
        self.max_time = max_time
        self.max_loc = max_loc
        self._percept_history = {}

    def get(self, location, time):
        return

    def add(self, percept, location, time):
        return
