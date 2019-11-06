from States.MultiAgentState import MultiAgentState


class ODState(MultiAgentState):
    def __init__(self, problem_instance, single_agent_states, next_to_move=0, pre_state=None, parent=None,
                 time_step=0, heuristic="Manhattan"):
        super().__init__(problem_instance, single_agent_states, parent=parent, time_step=time_step, heuristic=heuristic)
        self._problem_instance = problem_instance
        if pre_state is None:
            self._pre_state = self     # Previous Intermediate State
        else:
            self._pre_state = pre_state
        self._next_to_move = next_to_move   # Next Agent To Move

    def get_paths_to_parent(self):
        paths = []
        for single_state in self._single_agents_states:
            paths.append(single_state.get_path_to_parent())
        return paths

    def expand(self, verbose=False):
        if verbose:
            print("Expansion in progress...", end=' ')

        state_to_expand = self.get_single_agent_states()[self._next_to_move]
        expanded_states_list = state_to_expand.expand()

        candidate_list = []
        for state in expanded_states_list:
            single_agent_states = self.clone_states()
            single_agent_states[self._next_to_move] = state

            if self.next_next_to_move() == 0:
                s = ODState(self._problem_instance, single_agent_states, next_to_move=self.next_next_to_move(),
                            pre_state=self._pre_state, parent=self, time_step=self.time_step()+1, heuristic=self._heuristic)
            elif self.next_next_to_move() == 1:
                s = ODState(self._problem_instance, single_agent_states, next_to_move=self.next_next_to_move(),
                            pre_state=self, parent=self, time_step=self.time_step(), heuristic=self._heuristic)
            else:
                s = ODState(self._problem_instance, single_agent_states, next_to_move=self.next_next_to_move(),
                            pre_state=self._pre_state, parent=self, time_step=self.time_step(), heuristic=self._heuristic)

            if s.is_a_standard_state():
                if not s.is_conflict(s._pre_state.get_single_agent_states()):
                    candidate_list.append(s)
            else:
                candidate_list.append(s)

        if verbose:
            print("DONE! Number of expanded states:", len(candidate_list))

        return candidate_list

    def next_next_to_move(self):
        if self._next_to_move+1 >= len(self._problem_instance.get_agents()):
            return 0
        else:
            return self._next_to_move+1

    def goal_test(self):
        if self.is_a_standard_state():
            return super().goal_test()
        return False

    def is_a_standard_state(self):
        return self._next_to_move == 0