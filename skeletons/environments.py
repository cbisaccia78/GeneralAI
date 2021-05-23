from random import randint
from copy import deepcopy, copy

from skeletons.spaces import Grid2D
from skeletons.states import StateNode
import numpy as np

from skeletons.states import State
from skeletons.things import Thing


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
        return state_node

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
            return new_state_node
        return None

    def gen_future_states(self, state_node, actions, actuators):
        """
            specifies transition model.
            :param state_node:
            :param actions:
            :param actuators:
            :return: new_state_node
        """
        # ss_set_list = str([state.Location.data for state in self.ss_set])

        print(str(state_node.state.Location.data) + '    ' + str(len(self.ss_set)))
        for action in actions:
            valid_actuator = None
            for actuator in actuators:
                if action.name in actuator.actions:
                    valid_actuator = actuator
                    break
            if not valid_actuator:
                continue
            future_state_node = self.result(state_node=state_node, action=action, actuator=valid_actuator)
            if future_state_node and not State.is_in(future_state_node.state, self.ss_set):
                future_state_node.prev_action = action
                future_state_node.prev_state_node = state_node
                state_node.future_state_nodes.append(future_state_node)
                self.ss_set.append(future_state_node.state)

    def _generate_state_space(self, node, depth, depth_limit):
        if depth_limit:
            if depth == depth_limit:
                return
        self.gen_future_states(
            state_node=node,
            actions=self.local_agent.actions(node.state),
            actuators=self.local_agent.actuators
        )
        if not node.future_state_nodes:
            return
        for future_node in node.future_state_nodes:
            self._generate_state_space(future_node, depth=depth+1, depth_limit=depth_limit)
        """
        :param head:
        :param depth:
        :return:
        """
        return

    def generate_state_space(self, agent, depth=None, method=None, args=None):
        """
        num_states = sum_i(sum_j(thing_ij * num_values_thing_ij*)) for j ranging over all things in state i
        :param starter: initial node
        :param depth: specifies how deep the state space tree will go. None for exhaustion
        :return:
        """
        self.local_agent = agent
        self.ss_head = deepcopy(agent.curr_state_node)
        if method:
            self.ss_head = method(agent.curr_state_node, args)
        self._generate_state_space(self.ss_head, depth=0, depth_limit=depth)
        self.ss_set = []
        return copy(self.ss_head)

    def start_agents(self):
        for agent_name in self.agents:
            for agent in self.agents[agent_name]:
                self.generate_state_space(agent)
                agent.agent_program()  # this needs to be multi threaded


class GridEnv2D(Environment):
    def __init__(self, col, row, name=None, rules=None):
        super(GridEnv2D, self).__init__(name, rules)
        self.allowed_agents = {'BasicProblemSolver': col + row}
        self.allowed_actions = {'Left', 'Right', 'Up', 'Down'}
        self.state = State(things=[Grid2D(columns=col, rows=row)])
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
        if state_node is None or state_node.state is None or state_node.state.Location is None:
            return False
        loc = state_node.state.Location.data
        x = loc[0]
        y = loc[1]
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
        dims = self.state.Grid2D.grid.shape
        local = Grid2D(columns=dims[0], rows=dims[1])
        dirty = self.state.Grid2D.grid[loc[0]][loc[1]]
        local.grid[loc[0]][loc[1]] = dirty
        loc_state = State(things=[Thing(name="Location", data=loc), Thing(name="dirty", data=dirty)])
        self.add_agents(agent)
        return StateNode(prev_state_node=None, prev_action=None, state=loc_state) if loc else None

    def world_state_so_far(self, state_node):
        s = state_node.state.Location.data
        d = state_node.state.dirty.data
        s_x = s[0]
        s_y = s[1]
        local = Grid2D(columns=self.max_x, rows=self.max_y)  # filled with 0.5 for unassigned
        local.grid[s_x][s_y] = d
        temp = state_node.prev_state_node
        while temp:
            s = temp.state.Location.data
            d = temp.state.dirty.data
            s_x = s[0]
            s_y = s[1]
            local.grid[s_x][s_y] = d
            temp = temp.prev_state_node



    def randomize_grid(self):
        dims = self.state.Grid2D.grid.shape
        self.state.Grid2D.grid = np.random.default_rng().integers(2, size=(dims[0], dims[1]))

    def handle_actuator(self, state_node, action, actuator):
        new_state = deepcopy(state_node)
        if action.name in self.allowed_actions:
            new_state = actuator.act(action=action, state_node=new_state)
        else:
            new_state = super(GridEnv2D, self).handle_actuator(new_state, action, actuator)
        return new_state
        # possibly contain a list of actuators and handlers for each actuator


class VacuumWorld(GridEnv2D):
    def __init__(self, col, row, name=None):
        super().__init__(col, row, name)
        self.randomize_grid()
        self.allowed_agents["Vacuum"] = col + row
        self.allowed_actions = {'Suck', 'Left', 'Right', 'Up', 'Down'}
        self.rules.add(self.one_agent_one_square)

    def assign_initial_state(self, agent):
        node = super(VacuumWorld, self).assign_initial_state(agent) # agent will have a location
        agent_loc = node.state.Location
        """
        following code assumes that space contains dirt only. need to modify
        for grid locations which can contain more than one thing.
        """
        node.state.on_dirt = self.space[agent_loc[0]][agent_loc[1]]
        return node

    def handle_actuator(self, state_node, action, actuator):
        if action.name in self.allowed_actions:
            new_state = actuator.act(action=action, state=state_node)
            self.space[new_state.location[0]][new_state.location[1]] = new_state.on_dirt
        else:
            new_state = super(VacuumWorld, self).handle_actuator(state_node, action, actuator)

        return new_state

