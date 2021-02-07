class Goal:
    def __init__(self, name=None):
        self.name = name
        self.states = []

    def achieved(self, state):
        if state in self.states:
            return True
        return False
