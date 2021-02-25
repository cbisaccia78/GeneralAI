from random import randint

from skeletons.spaces import Grid2D
from skeletons.states import State, StateNode
import numpy as np

from skeletons.states import State
from skeletons.things import Thing


class Environment:
    def __init__(self, *args):
        self.allowed_agents = None
        self.agents = {}
        self.actuators = set()
        self.space = None
        self.rules = None

    def step(self):
        """
        time = time + time_unit in whatever sense time_unit is implemented
        :return:
        """
        return

    def start(self, steps=-1):
        """
        time = time_unit_0 iren whatever sense time_unit is implemented
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
        for action in actions:
            valid_actuator = None
            for actuator in actuators:
                if action.name in actuator.actions:
                    valid_actuator = actuator
                    break
            if not valid_actuator:
                continue
            future_state_node = self.result(state_node=state_node, action=action, actuator=valid_actuator)
            if future_state_node:
                state_node.future_state_nodes.append(future_state_node)


class GridEnv2D(Environment):
    def __init__(self, col, row, name=None, rules=None):
        self.name = name
        self.allowed_agents = {'BasicProblemSolver': col + row}
        self.allowed_actions = {'Left', 'Right', 'Up', 'Down'}
        self.agents = {}
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
        if state_node is None or state_node.state is None or state_node.state.location is None:
            return False
        loc = state_node.state.location
        x = loc[0]
        y = loc[1]
        if 0 < x < self.max_x:
            if 0 < y < self.max_y:
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
            return (randint(0,num_rows-1), randint(0,num_cols-1))
        for y in range(0,num_rows):
            for x in range(0,num_cols):
                for key in self.agents:
                    for agent in self.agents[key]:
                        if (y,x) != agent.curr_state_node.state.location:
                            return (y,x)
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
        loc_state = State(things=[Thing(name="Location", data=loc)])
        self.add_agents(agent)
        return StateNode(prev_state_node=None, prev_action=None, state=loc_state) if loc else None

    def assign_initial_local(self, agent):
        """
        shear off all space information except in the location that
        the agent currently resides and return new env
        :param agent:
        :return: subspace of the global environment containing only the agent
        """
        dims = self.state.Grid2D.grid.shape
        agent_loc = agent.curr_state_node.state.Location.data
        local = GridEnv2D(col=dims[0], row=dims[1])
        local.state.Grid2D.grid[agent_loc[0]][agent_loc[1]] = self.state.Grid2D.grid[agent_loc[0]][agent_loc[1]]
        local.agents[repr(agent)] = [agent]
        return local

    def randomize_grid(self):
        dims = self.state.Grid2D.grid.shape
        self.state.Grid2D.grid = np.random.default_rng().integers(2, size=(dims[0], dims[1]))

    def handle_actuator(self, state_node, action, actuator):
        if action.name in self.allowed_actions:
            new_state = actuator.act(action=action, state=state_node)
        else:
            new_state = super(GridEnv2D, self).handle_actuator(state_node, action, actuator)
        return new_state
        # possibly contain a list of actuators and handlers for each actuator


class VacuumWorld(GridEnv2D):
    def __init__(self, col, row, name=None):
        super().__init__(col, row, name)
        self.randomize_grid()
        self.allowed_agents["Vacuum"] = col + row
        self.allowed_actions = {'Suck'}
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
        else:
            new_state = super(VacuumWorld, self).handle_actuator(state_node, action, actuator)

        return new_state

