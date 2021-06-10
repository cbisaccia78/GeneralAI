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

    def act(self, action, state_node):
        if action.name not in self.actions:
            return state_node
        if 'location' not in vars(state_node.state):
            return state_node
        if action.name == 'Left':
            state_node.state.location[0] -= action.units
        elif action.name == 'Right':
            state_node.state.location[0] += action.units
        elif action.name == 'Up':
            state_node.state.location[1] -= action.units
        elif action.name == 'Down':
            state_node.state.location[1] += action.units

        return state_node


class Sucker(Actuator):
    def __init__(self):
        super(Sucker, self).__init__()
        self.actions.add('Suck')

    def act(self, action, state):
        if state.grid2d.grid[0][]:
            state.on_dirt = 0
            return state
        return state



