class Goal:
    def __init__(self, states, name=None):
        self.name = name
        self.states = states

    def test(self, state):
        if state in self.states:
            return True
        return False


class Location(Goal):
    pass


