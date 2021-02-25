from skeletons.things import Thing


class Percept:
    def __init__(self, thing_list):
        self.observations = thing_list


class Percepts(object):
    def __init__(self, max_time=-1, max_loc=None):
        self.max_time = max_time
        self.max_loc = max_loc

    def get(self, location, time):
        return

    def add(self, percept: Percept, location, time):
        return
