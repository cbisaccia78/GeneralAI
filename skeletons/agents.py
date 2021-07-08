from skeletons.actions import Left, Right, Up, Down, Suck
from skeletons.problems import Problem
from skeletons.percepts import Percepts
from skeletons.helpers import basic_eval, path_cost, depth_cost, is_cycle
from functools import lru_cache



class Agent:
    def __init__(self, name=None, environment=None):
        self.name = name
        self.sensors = None
        self.percept_history = Percepts()
        self.actuators = None
        self.environment = environment
        self.curr_state_node = self.get_initial_state()
        self.ss_head = None

    def __repr__(self):
        return self.__class__.__name__

    def update_local_env(self, percepts):
        self.percept_history.extend(percepts)

    def get_initial_state(self):
        if self.environment:
            return self.environment.assign_initial_state(self)

    def get_local_env(self):
        if self.environment:
            return self.environment.assign_initial_local(self)

    def sense(self):
        """
        :return:
        """
        for sensor in self.sensors:
            self.percept_history[(self.curr_state_node.state.location, self.environment.time)] = sensor.sense()


class BasicProblemSolver(Agent):
    """
    Searches sequentially at each layer for a solution to specified problem in particular environment
    """
    def __init__(
            self, environment=None,
            name=None,
            closed_loop=True,
            goal_states=None,
            step_cost=None,
            actuators=None,
            sensors=None,
    ):
        super(BasicProblemSolver, self).__init__(name, environment)
        self.actuators = actuators
        self.sensors = [sensor(agent=self) for sensor in sensors]
        self.closed_loop = closed_loop  # AKA: self.eyes_open = eyes_open
        self.step_cost=step_cost
        self.problem = Problem(initial_state=self.curr_state_node.state, goal_states=goal_states, step_cost=step_cost)
        self.frontier = []
        self.reached = {}
        self.stat_string = ""

    def actions(self, state):
        properties = [prop for prop in vars(state) if not prop.startswith(("__"))]
        action_list = []
        for prop in properties:
            if prop == "location":
                action_list.extend([Left(), Right(), Up(), Down()])
            if prop == 'vacuum':
                action_list.extend([Suck()])
        return action_list

    def agent_program(self):
        """
        Once called, agent goes through a loop of sense <-> act <-> goal_test
        """
        if self.closed_loop:
            # need to research after each sense
            while not self.problem.test(self.curr_state_node):
                self.sense()
                for k in self.percept_history:
                    print(self.percept_history[k])
                self.act()
            return True
        else:
            # eyes closed
            #print('_______________')
            #print(self.environment.state.grid2d.grid)
            #print('_______________')
            loc = self.curr_state_node.state.location
            #print(f'x = {loc[1]}, y = {loc[0]}')
            #print(self.curr_state_node.state.grid2d.grid)
            solution = self.search()
            if solution:
                node = solution
                action_list = []
                
                while node.parent:
                    '''done in a for loop to simulate time, instead of just doing curr_state_node = solution[-1]
                    need to find a way to incorporate time into state transitions'''
                    self.curr_state_node = node
                    action_list.append(node.prev_action)
                    node = node.parent
                action_list.reverse()
                print(action_list)
                return

    def act(self):
        """
        add the percepts to the agents history,
        then search the state space for action(s) which will satisfy goal
        after actions found, pass each action to its respective actuator
        :param percepts:
        :return:
        """
        solution = self.search()
        if solution:
            self.curr_state_node = solution[0]

    def breadth_first_search(self, initial_node, depth_limit):
        goal = self.problem.test(initial_node.state)
        if depth_limit == 0:
            return goal
        future_nodes = self.environment.gen_future_nodes(initial_node, self.actions(initial_node.state), self.actuators,
                                                         self.step_cost)
        self.frontier.extend(future_nodes) # f is just depth of tree so no need to sort
        self.reached = {initial_node.state} # can avoid hash table because no redundant paths
        count = 0
        count += len(future_nodes)
        while len(self.frontier) > 0:
            node = self.frontier.pop()
            for child in self.expand(node):
                count += 1
                if self.problem.test(child.state): # can test as soon as generated, because no redundant paths
                    self.stat_string += f"{count},"
                    return node
                s = child.state
                if s not in self.reached:
                    self.reached.add(s)
                    self.frontier.append(child)  # ToDo need to make sure this child is placed in correct order
        self.stat_string += f"{count},"
        return None

    def best_first_search(self, initial_node, depth_limit, f=basic_eval):
        goal = self.problem.test(initial_node.state)
        if depth_limit == 0:
            return goal
        future_nodes = self.environment.gen_future_nodes(initial_node, self.actions(initial_node.state), self.actuators, self.step_cost)
        self.frontier.extend(sorted(future_nodes, key=f))
        self.reached = {initial_node.state: initial_node}
        count = 0
        count += len(future_nodes)
        while len(self.frontier) > 0:
            node = self.frontier.pop()
            if self.problem.test(node.state):
                self.stat_string += f"{count},"
                return node
            for child in self.expand(node):
                s = child.state
                if s not in self.reached or child.path_cost < self.reached[s].path_cost:
                    self.reached[s] = child
                    self.frontier.append(child)  # ToDo need to make sure this child is placed in correct order
                count += 1
        self.stat_string += f"{count},"
        return None

    def depth_first_search(self, initial_node, depth_limit):
        goal = self.problem.test(initial_node.state)
        if depth_limit == 0:
            return goal
        future_nodes = self.environment.gen_future_nodes(initial_node, self.actions(initial_node.state), self.actuators,
                                                         self.step_cost)
        self.frontier.extend(future_nodes)  # LIFO stack
        while len(self.frontier) > 0:
            node = self.frontier.pop(-1)
            if self.problem.test(node.state):
                return node
            if node.depth <= depth_limit:
                if not is_cycle(node, depth_limit):
                    for child in self.expand(node):
                        self.frontier.append(child)
        return None

    def iterative_deepening(self, initial_node, iter_max):
        #  does initial node need to be recreated for each search?
        for i in range(0, iter_max):
            solution = self.depth_first_search(initial_node, i)
            if solution:
                return solution
        return None

    def a_star(self, initial_node, depth_limit, h):
        return

    def expand(self, node):
        return self.environment.gen_future_nodes(node, self.actions(node.state), self.actuators, self.step_cost)

    def search(self, depth=None, search_type="id", iter_max=10000, h=None):
        """
        makes use of self.problem: provides filtering of environment into a relevant set of features (state space),
        coupled with a path cost function, a goal evaluation function, and much much more!
        Can currently only search from the agents current state.
        :param depth: if depth == None then it searches the whole state space
        :param search_type: defaults to best first search
        :param iter_max: how far to go for iterative deepening
        :returns: sequence of actions that define a solution.
        """
        if search_type == "dijkstra":
            return self.best_first_search(self.curr_state_node, depth_limit=depth, f=path_cost)
        elif search_type == "bidijkstra":
            return self.bidirectionalBF(self.curr_state_node, self.problem.goal_states, )
        elif search_type == 'dfs':
            return self.best_first_search(self.curr_state_node, depth_limit=depth, f=depth_cost)
        elif search_type == 'id':
            return self.iterative_deepening(self.curr_state_node, iter_max=iter_max)
        elif search_type == 'a_star':
            if h is None:
                return None
            return self.a_star(self.curr_state_node, depth_limit=depth, h=h)
        else:
            return self.breadth_first_search(self.curr_state_node, depth_limit=depth)


class PokerPlayer(BasicProblemSolver):
    def __init__(
            self,
            environment=None,
            name=None,
            closed_loop=True,
            goal_states=None,
            step_cost=None,
            actuators=None,
            sensors=None,
    ):
        super(PokerPlayer, self).__init__(name, environment, closed_loop, goal_states, step_cost, actuators, sensors)



class BasicUtility(Agent):
    pass


class TableDrivenAgent(Agent):
    def __init__(self, name, environment):
        super().__init__(name=name, environment=environment)
        self.tabulator = {}

    def agent_program(self, percept):
        """
        In the context of the brain-arm-bottle example, the brain would be the implementation of the agent function.
        ie) it takes a percept sequence(memory) and maps it to a given action (electrical/chemical impulse sent to the body)
        :param percept:
        :return:
        """
        self.percept_history.append(percept)
        return self.tabulator[self.percept_history]








