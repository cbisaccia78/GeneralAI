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
        if 'Location' not in vars(state):
            return None
        if action == 'Left':
            state.Location[0] -= action.units
        elif action == 'Right':
            state.Location[0] += action.units
        elif action == 'Up':
            state.Location[1] -= action.units
        elif action == 'Down':
            state.Location[1] += action.units
        else:
            return None

