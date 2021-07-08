from random import randint
from copy import deepcopy, copy

from skeletons.spaces import Grid2D
from skeletons.states import StateNode
import numpy as np

from skeletons.states import State


class Environment:
    def __init__(self, *args):
        self.allowed_agents = None
        self.agents = {}
        self.local_agent = None
        self.actuators = set()
        self.space = None
        self.rules = None
        self.ss_head = None
        self.ss_set = []
        self.time = 0

    def step(self):
        """
        time = time + time_unit in whatever sense time_unit is implemented
        :return:
        """
        return

    def start(self, steps=-1):
        """
        time = time_unit_0 in whatever sense time_unit is implemented
        :param steps: increments of time, if -1 go till infinity
        :return:
        """
        return

    def add_agents(self, agents):
        """
        check to see if agents are allowed and then add them
        :param agents:
        :return:
        """
        if self.validate_agents(agents):
            if not isinstance(agents, list):
                agents = [agents]

            for agent in agents:
                agent_name = repr(agent)
                if agent_name in self.agents:
                    self.agents[agent_name] += agent
                else:
                    self.agents[agent_name] = [agent]

    def validate_agents(self, agents):
        """
        check to see if agent class names exist in self.allowed_agents
        :param agents:
        :return:
        """
        if not self.allowed_agents:
            raise Exception()

        if isinstance(agents, list):
            for agent in agents:
                if repr(agent) not in self.allowed_agents:
                    raise Exception()
            return True

        if repr(agents) in self.allowed_agents:
            return True

        raise Exception()

    def assign_initial_state(self, agent):
        """
        determine the local state of the particular agent in the environment, specific to agents particular problem
        :param agent:
        :return:
        """
        return

    def assign_initial_local(self, agent):
        """
                This function will need to be overridden for every specific environment
        """
        return

    def handle_actuator(self, state_node, action, actuator):
        """
               This function will need to be overridden for every specific environment
               :param state_node:
               :param action:
               :param actuator:
               :return:
               """
        # fn = StateNode(parent=state_node, prev_action=state_node.action, state=state_node.state, path_cost=state_node.path_cost)
        fn = deepcopy(state_node)
        if action.name in self.allowed_actions:
            fn = actuator.act(action=action, state_node=fn)
        else:
            fn = super(GridEnv2D, self).handle_actuator(fn, action, actuator)
        return fn

    def passes(self, state_node, rule):
        return rule(state_node)

    def valid(self, state_node):
        for rule in self.rules:
            if not self.passes(state_node, rule):
                return False
        return True

    def result(self, state_node, action, actuator):
        new_state_node = self.handle_actuator(state_node=state_node, action=action, actuator=actuator)
        if self.valid(new_state_node):
            return self.post_handle(new_state_node, action)
        return None

    def gen_future_nodes(self, state_node, actions, actuators, step_cost, direction=1):
        """
            specifies transition model.
            :param state_node:
            :param actions:
            :param actuators:
            :param step_cost:
            :param direction: allow for bidirectional search
            :return: new_state_node
        """
        # ss_set_list = str([state.Location.data for state in self.ss_set])

        future_nodes = [] # priority queue
        for action in actions:
            valid_actuator = None
            for actuator in actuators:
                if action.name in actuator.actions:
                    valid_actuator = actuator
                    break
            if not valid_actuator:
                continue
            fn = self.result(state_node=state_node, action=action, actuator=valid_actuator)
            if fn:
                fn.prev_action = action
                fn.parent = state_node
                fn.path_cost = state_node.path_cost + step_cost(state_node.state, fn.prev_action, fn.state)
                fn.depth = state_node.depth + direction
                future_nodes.append(fn)

        return future_nodes

    def start_agents(self):
        for agent_name in self.agents:
            for agent in self.agents[agent_name]:
                agent.agent_program()  # this needs to be multi threaded

    def post_handle(self, fn, action):
        return fn


class PokerTable(Environment):

    def __init__(self, players=[], sb=1, bb=2, min_buy=60, max_buy=300, max_seats=9, straddle_allowed=True):
        super(PokerTable, self).__init__()
        self.players = players
        self.small_blind = sb
        self.big_blind = bb
        self.min_buy_in = min_buy
        self.max_buy_in = max_buy
        self.straddle_allowed = straddle_allowed
        self.allowed_agents = {'PokerPlayer': max_seats}
        self.allowed_actions = {'Bet', 'Fold', 'Call', 'Raise', 'Rebuy', 'Addon'}
        self.rules = {self.valid_wager}
        self.init_table()

    def init_table(self):
        if len(self.players) == 0:
            return


    def valid_wager(self, node):
        s = node.state
        if node is None or s is None:
            return False
        if s.stack_size < 0 or s.bankroll < 0:
            return False
        return True


class GridEnv2D(Environment):
    def __init__(self, col, row, name=None, rules=None):
        super(GridEnv2D, self).__init__(name, rules)
        self.allowed_agents = {'BasicProblemSolver': col + row}
        self.allowed_actions = {'Left', 'Right', 'Up', 'Down'}
        self.state = State(grid2d=Grid2D(columns=col, rows=row))
        self.max_x = col
        self.max_y = row
        self.rules = {self.on_board}
        if rules:
            for rule in rules:
                self.rules.add(rule)
    """
    *
    *
    * rules:
    """
    def on_board(self, state_node):
        if state_node is None or state_node.state is None or state_node.state.location is None:
            return False
        loc = state_node.state.location
        y = loc[0]
        x = loc[1]
        if -1 < x < self.max_x:
            if -1 < y < self.max_y:
                return True
        return False

    def one_agent_one_square(self, state_node):
        # should we assume on_board rule has already been verified?
        for key in self.agents:
            for agent in self.agents[key]:
                if state_node.state.location == agent.curr_state_node.state.location:
                    return False
        return True

    def for_util(self, num_rows, num_cols):
        if not self.agents:
            return [randint(0,num_rows-1), randint(0,num_cols-1)]
        for y in range(0,num_rows):
            for x in range(0,num_cols):
                for key in self.agents:
                    for agent in self.agents[key]:
                        if [y, x] != agent.curr_state_node.state.location:
                            return [y, x]
        return None

    def assign_location(self, agent):
        # find empty x loc
        env_dims = (self.max_x, self.max_y)
        loc = self.for_util(num_rows=env_dims[1], num_cols=env_dims[0])
        return loc
        """
            THIS CODE COULD BE MORE EFFICIENT FOR MASSIVE GRIDS

            loc_found = False
            while True:
                loc_guess = (randint(0, num_rows-1), randint(0, num_cols-1))
                if loc_guess not in self.agent_coords:
                    break
        """

    def assign_initial_state(self, agent):
        loc = self.assign_location(agent)
        loc_state = State(location=loc, grid2d=Grid2D(self.max_x, self.max_y))
        self.add_agents(agent)
        return StateNode(parent=None, prev_action=None, state=loc_state) if loc else None

    def world_state_so_far(self, state_node):
        s = state_node.state.location
        d = state_node.state.dirty
        s_x = s[0]
        s_y = s[1]
        local = Grid2D(columns=self.max_x, rows=self.max_y)  # filled with 0.5 for unassigned
        local.grid[s_x][s_y] = d
        temp = state_node.parent
        while temp:
            s = temp.state.location
            d = temp.state.dirty
            s_x = s[0]
            s_y = s[1]
            local.grid[s_x][s_y] = d
            temp = temp.parent
        return State(grid2d=local)

    def randomize_grid(self):
        dims = self.state.grid2d.grid.shape
        self.state.grid2d.grid = np.random.default_rng().integers(2, size=(dims[0], dims[1]))

    def handle_actuator(self, state_node, action, actuator):
        #fn = StateNode(parent=state_node, prev_action=state_node.action, state=state_node.state, path_cost=state_node.path_cost)
        fn = deepcopy(state_node)
        if action.name in self.allowed_actions:
            fn = actuator.act(action=action, state_node=fn)
        else:
            fn = super(GridEnv2D, self).handle_actuator(fn, action, actuator)
        return fn

        # possibly contain a list of actuators and handlers for each actuator


class VacuumWorld(GridEnv2D):
    def __init__(self, col, row, name=None):
        super().__init__(col, row, name)
        self.randomize_grid()
        self.allowed_agents["Vacuum"] = col + row
        self.allowed_actions = {'Suck', 'Left', 'Right', 'Up', 'Down'}
        # self.rules.add(self.one_agent_one_square)

    def assign_initial_state(self, agent):
        loc = self.assign_location(agent)
        gr = Grid2D(self.max_x, self.max_y)
        has_dirt = self.state.grid2d.grid[loc[0]][loc[1]]
        gr.grid[loc[0]][loc[1]] = has_dirt
        loc_state = State(location=loc, grid2d=gr, vacuum=True)
        self.add_agents(agent)
        return StateNode(parent=None, prev_action=None, state=loc_state) if loc else None

    def post_handle(self, fn, action):
        if action in ['Left', 'Right', 'Up', 'Down']:
            loc = fn.state.location
            fn.state.grid2d.grid[loc[0]][loc[1]] = self.state.grid2d.grid[loc[0]][loc[1]]
        return fn





