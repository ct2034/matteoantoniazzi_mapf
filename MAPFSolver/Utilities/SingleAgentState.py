"""
Class representing a single agent state. It stores the agent position at a specific time step. As superclass of State it
has a g-value, an h-value, and the sum f-value.
"""
from MAPFSolver.Utilities.SolverSettings import SolverSettings
from Utilities.State import State


class SingleAgentState(State):
    def __init__(self, map, agent_id, goal, position, path_cost, solver_settings, parent=None, time_step=0,
                 remaining_ts_in_goal=None, allowed_to_move=True):
        super().__init__(parent, time_step)
        self._map = map
        self._agent_id = agent_id
        self._position = position
        self._goal = goal
        self._solver_settings = solver_settings
        self._allowed_to_move = allowed_to_move  # False if the agent is in the goal and cannot move from there
                                                 # Start decrementing the goal occupation timer
        self._remaining_ts_in_goal = solver_settings.get_goal_occupation_time() \
            if remaining_ts_in_goal is None else remaining_ts_in_goal
        self._g = path_cost
        self.compute_heuristics()

    def expand(self, verbose=False):
        """
        Expand the current state. It computes the possible neighbour positions and creates a state for each new possible
        position. In addition of the neighbours we add the possibility to remain in the same position, obviously the
        time-step will be incremented and the cost of the wait move is equal to the cost to move, that is 1.
        If the state is a goal state we start decrementing a variable which keep count of the time spent in the goal.
        If the state is a goal state and the agent has been in the goal for the time needed (defined by
        GOAL_OCCUPATION_TIME) the state is a completed state and the expansion return itself.
        :return: the list of possible next states.
        """
        expanded_nodes_list = []

        if self.goal_test():
            if self.is_completed():
                return [self.clone_state()]  # Time_step remain blocked so once arrived it doesn't block others
            else:
                if not self._allowed_to_move:
                    return [SingleAgentState(self._map, self._agent_id, self._goal, self._position, self._g,
                                             self._solver_settings, parent=self, time_step=self._time_step+1,
                                             remaining_ts_in_goal=self._remaining_ts_in_goal-1,
                                             allowed_to_move=False)]
                else:
                    # Return one state that consider the fact that the agent has reached the goal and will never move from
                    # there and consider the fact that he can still move so all the neighbours and stay in the goal but
                    # paying the cost.
                    expanded_nodes_list.append(SingleAgentState(self._map, self._agent_id, self._goal, self._position,
                                                                self._g, self._solver_settings, parent=self,
                                                                time_step=self._time_step+1,
                                                                remaining_ts_in_goal=self._remaining_ts_in_goal-1,
                                                                allowed_to_move=False))

        expanded_nodes_list.append(self.wait_state())
        possible_moves = self._map.get_neighbours_xy(self._position)
        for i in possible_moves:
            expanded_nodes_list.append(SingleAgentState(self._map, self._agent_id, self._goal, i, self._g+1,
                                                        self._solver_settings, parent=self,
                                                        time_step=self._time_step+1))
        return expanded_nodes_list

    def expand_optimal_policy(self):
        """
        Compute the next state if we follow the optimal policy, so without keep account of conflicts with other agents.
        If the state is a goal state we start decrementing a variable which keep count of the time spent in the goal.
        If the state is a goal state and the agent has been in the goal for the time needed (defined by
        GOAL_OCCUPATION_TIME) the state is a completed state and the expansion return itself.
        :return: the next state following the optimal policy
        """
        if self.goal_test():
            if self.is_completed():
                return self.clone_state()   # Time_step remain blocked so once arrived it doesn't block others
            else:
                return SingleAgentState(self._map, self._agent_id, self._goal, self._position, self._g,
                                        self._solver_settings, parent=self, time_step=self._time_step+1,
                                        remaining_ts_in_goal=self._remaining_ts_in_goal - 1)

        next_node = self.get_next_optimal_state()

        return next_node

    def get_next_optimal_state(self):
        """
        Compute the next optimal state following the optimal policy.
        :return: the next state following the optimal policy
        """
        from Utilities.AStar import AStar
        solver = AStar(SolverSettings())  # Forse serve il goal occupation time generale
        path = solver.find_path(self._map, self._position, self._goal)
        next_pos = path[1]
        return SingleAgentState(self._map, self._agent_id, self._goal, next_pos, self._g+1, self._solver_settings,
                                parent=self, time_step=self._time_step+1)

    def compute_heuristics(self):
        self._h = self._solver_settings.get_heuristic_object().compute_heuristic(self._position, self._goal)

    def calculate_cost(self):
        if self.is_root():
            self._g = 0
        else:
            self._g = self.predecessor().g_value() + 1
        return

    def wait_state(self):
        return SingleAgentState(self._map, self._agent_id, self._goal, self._position, self._g + 1, self._solver_settings,
                                parent=self, time_step=self._time_step+1,
                                remaining_ts_in_goal=self._remaining_ts_in_goal)

    def goal_test(self):
        return self._position == self._goal

    def is_completed(self):
        if self._solver_settings.stay_in_goal():
            return self.goal_test()
        return self.goal_test() and self._remaining_ts_in_goal == 1

    def get_position(self):
        return self._position

    def get_path_to_parent(self):
        print(self._position)
        path = []
        node = self
        while node._parent is not None:
            path.append(node._position)
            node = node._parent
        path.append(node._position)
        path.reverse()
        return path

    def get_agent_id(self):
        return self._agent_id

    def clone_state(self):
        return SingleAgentState(self._map, self._agent_id, self._goal, self._position, self._g, self._solver_settings,
                                parent=self._parent, time_step=self._time_step,
                                remaining_ts_in_goal=self._remaining_ts_in_goal, allowed_to_move=self._allowed_to_move)

    def equal_position(self, other):
        assert isinstance(other, SingleAgentState)
        return self._position == other._position

    def equal(self, other):
        assert isinstance(other, SingleAgentState)
        return self._position == other._position and self._time_step == other._time_step

    def __str__(self):
        string = ''
        string = string + ' [AGENT ID: ' + str(self._agent_id) + ' F: ' + str(self.f_value()) + ' '\
                 + str(self._position) + ' TS:' + str(self.time_step()) + '] '
        return string
