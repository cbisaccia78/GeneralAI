from random import randint

from skeletons.spaces import Grid2D
from skeletons.states import State, StateNode
import numpy as np

from skeletons.states import State


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

    def passes(self, state_node, rule):
        return rule(state_node)

    def valid(self, state_node):
        for rule in self.rules:
            if not self.passes(state_node, rule):
                return False
        return True

    def result(self, state_node, action, actuator):
        new_state = actuator.act(action, state_node)
        if self.valid(new_state):
            return new_state
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
                if action in actuator.actions:
                    valid_actuator = actuator
                    break
            if not valid_actuator:
                continue
            future_state = self.result(state_node=state_node, action=action, actuator=valid_actuator)
            if future_state:
                state_node.future_state_nodes.append(
                    StateNode(prev_state_node=self, prev_action=action, state=future_state))


class GridEnv2D(Environment):
    def __init__(self, col, row, name=None):
        self.name = name
        self.allowed_agents = {'BasicProblemSolver': col + row}
        self.agents = {}
        self.agent_coords = set()
        self.state = State(things=[Grid2D(columns=col, rows=row)])
        self.max_x = col
        self.max_y = row
        self.rules = {self.on_board}

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

    def for_util(self, num_rows, num_cols):
        for y in num_rows:
            for x in num_cols:
                if (y,x) not in self.agent_coords:
                    return (y,x)
        return None

    def assign_location(self, agent):
        # find empty x loc
        env_dims = self.state.Grid2D.shape
        loc = self.for_util(env_dims[0], env_dims[1])
        if loc:
            self.agent_coords.add(loc)
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
        return StateNode(prev_state_node=None, prev_action=None, state=loc) if loc else None

    def assign_initial_local(self, agent):
        return


class VacuumWorld(GridEnv2D):
    def __init__(self, col, row, name=None):
        super().__init__(col, row, name)
        self.allowed_agents["Vacuum"] = col + row
        self.rules.add(self.one_agent_one_square)

    def one_agent_one_square(self, state_node):
        return True

    def result(self, state_node, action, actuator):
        new_state = actuator.act(action, state_node)
        if self.valid(new_state):
            return new_state
        return None


