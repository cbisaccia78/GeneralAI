class Actuator:
    """

    """
    def __init__(self):
        self.actions = set()
        return

    def act(self, action):
        # do
        return


class Mover(Actuator):
    def __init__(self):
        super(Mover, self).__init__()
        self.actions.add('Left')
        self.actions.add('Right')
        self.actions.add('Up')
        self.actions.add('Down')

    def act(self, action, state):
        if action not in self.actions:
            return None
        if action == 'Left':
            state

