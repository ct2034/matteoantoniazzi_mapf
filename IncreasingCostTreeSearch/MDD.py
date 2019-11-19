from IncreasingCostTreeSearch.MDDNode import MDDNode
from QueueStructures.MDDQueue import MDDQueue


class MDD:
    def __init__(self, map, agent, cost):
        self._map = map
        self._agent = agent
        self._cost = cost
        self._paths = []
        self._ending_nodes = []
        self._nodes = MDDQueue()
        self.build_mdd()

    def build_mdd(self):
        root = MDDNode(self._map, self._agent.get_start())
        self._nodes.add(root)

        frontier = MDDQueue()
        frontier.add(root)

        while not frontier.is_empty():
            frontier.sort_by_time_step()
            cur_node = frontier.pop()

            if cur_node.time_step() > self._cost:
                return

            if cur_node.time_step() == self._cost:
                if cur_node.position() == self._agent.get_goal():
                    self._ending_nodes.append(cur_node)
                    self._paths = cur_node.get_paths_to_parent()

            expanded_nodes = cur_node.expand()

            for node in expanded_nodes:
                if self._nodes.contains_node(node):
                    self._nodes.add_parent_to_node(node, cur_node)
                else:
                    frontier.add(node)
                    self._nodes.add(node)

    def get_paths(self):
        return self._paths
