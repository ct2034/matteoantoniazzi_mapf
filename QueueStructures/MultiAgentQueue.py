from States.MultiAgentState import MultiAgentState


class MultiAgentQueue:
    def __init__(self):
        self._queue = []

    def contains(self, item):
        assert isinstance(item, MultiAgentState)
        for state in self._queue:
            if state.equal_positions(item):
                return True
        return False

    def add(self, item):
        assert isinstance(item, MultiAgentState)
        self._queue.append(item)

    def add_list_of_states(self, state_list):
        self._queue.extend(state_list)

    def pop(self):
        return self._queue.pop(0)

    def is_empty(self):
        return len(self._queue) == 0

    def size(self):
        return len(self._queue)

    def sort_by_f_value(self):
        self._queue.sort(key=lambda x: x.f_value(), reverse=False)

    def __str__(self):
        string = ''
        for s in self._queue:
            string = string + '[' + str(s.get_position()) + ' TS:' + str(s.get_timestamp()) + ']'
        return string