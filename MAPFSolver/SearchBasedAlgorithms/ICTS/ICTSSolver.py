from MAPFSolver.Utilities.AbstractSolver import AbstractSolver
from MAPFSolver.Utilities.paths_processing import calculate_soc, calculate_makespan
from MAPFSolver.SearchBasedAlgorithms.ICTS.ICTNode import ICTNode
from MAPFSolver.SearchBasedAlgorithms.ICTS.ICTQueue import ICTQueue
import time


class ICTSSolver(AbstractSolver):
    """
    ICTS (Increasing Cost Tree Search) algorithm is a complete and optimal algorithm. It works in a two level way:
    - The high-level performs a search on a new search tree called increasing cost tree (ICT). Each node in the ICT
      consists of a k-vector [C 1 , C 2 , . . . C k ] which represents all possible solutions in which the cost of the
      individual path of each agent a i is exactly C i.
    - The low-level performs a goal test on each of these tree nodes.
    """

    def __init__(self, solver_settings):
        """
        Initialize the ICTS solver.
        :param solver_settings: settings used by the A* solver.
        """
        super().__init__(solver_settings)
        self._frontier = None
        self._closed_list = None
        self._n_of_generated_nodes = 0
        self._n_of_expanded_nodes = 0

    def solve(self, problem_instance, verbose=False, return_infos=False, time_out=None):
        """
        Solve the MAPF problem using the ICTS algorithm returning the paths as lists of list of (x, y) positions.
        """
        start = time.time()

        self.initialize_problem(problem_instance)

        while not self._frontier.is_empty():
            self._frontier.sort_by_cost()
            cur_state = self._frontier.pop()

            if time_out is not None:
                if time.time() - start > time_out:
                    break

            temp_time_out = None if time_out is None else time_out-(time.time() - start)
            cur_state.initialize_node(verbose=verbose, time_out=temp_time_out)

            if cur_state.is_goal():
                paths = cur_state.solution()
                soc = calculate_soc(paths, self._solver_settings.stay_at_goal(),
                                    self._solver_settings.get_goal_occupation_time())
                makespan = calculate_makespan(paths, self._solver_settings.stay_at_goal(),
                                              self._solver_settings.get_goal_occupation_time())
                output_infos = self.generate_output_infos(soc, makespan, self._n_of_generated_nodes,
                                                          self._n_of_expanded_nodes, time.time() - start)
                if verbose:
                    print("PROBLEM SOLVED: ", output_infos)

                if return_infos:
                    return paths, output_infos
                return paths

            """
            NORMAL
            """
            """if not self._closed_list.contains_node(cur_state):
                self._closed_list.add(cur_state)
                expanded_nodes = cur_state.expand()
                self._n_of_generated_nodes += len(expanded_nodes)
                self._n_of_expanded_nodes += 1
                self._frontier.add_list_of_nodes(expanded_nodes)"""

            """
            CASE 2
            """
            """self._closed_list.add(cur_state)
            expanded_nodes = cur_state.expand()

            expanded_nodes_not_in_closed_list = []
            for node in expanded_nodes:
                if not self._closed_list.contains_node(node):
                    expanded_nodes_not_in_closed_list.append(node)

            self._n_of_generated_nodes += len(expanded_nodes_not_in_closed_list)
            self._n_of_expanded_nodes += 1
            self._frontier.add_list_of_nodes(expanded_nodes_not_in_closed_list)"""

            """
            CASE 3
            """
            """if not self._closed_list.contains_node(cur_state):
                self._closed_list.add(cur_state)
                expanded_nodes = cur_state.expand()

                expanded_nodes_not_in_frontier = []

                for node in expanded_nodes:
                    if not self._frontier.contains_node(node):
                    
                        expanded_nodes_not_in_frontier.append(node)

                self._n_of_generated_nodes += len(expanded_nodes_not_in_frontier)
                self._n_of_expanded_nodes += 1
                self._frontier.add_list_of_nodes(expanded_nodes_not_in_frontier)"""

            """
            CASE 4
            """
            self._closed_list.add(cur_state)
            expanded_nodes = cur_state.expand()

            expanded_nodes_not_in_closed_list = []
            for node in expanded_nodes:
                if not self._closed_list.contains_node(node) and not self._frontier.contains_node(node):
                    expanded_nodes_not_in_closed_list.append(node)

            self._n_of_generated_nodes += len(expanded_nodes_not_in_closed_list)
            self._n_of_expanded_nodes += 1
            self._frontier.add_list_of_nodes(expanded_nodes_not_in_closed_list)

        if return_infos:
            return [], None
        return []

    def initialize_problem(self, problem_instance):
        """
        Initialize the frontier and the closed list for the given problem.
        """
        self._frontier = ICTQueue()
        self._closed_list = ICTQueue()
        self._n_of_generated_nodes = 1
        self._n_of_expanded_nodes = 0

        starter_state = ICTNode(problem_instance, self._solver_settings)

        self._frontier.add(starter_state)

    def __str__(self):
        return "Increasing Cost Tree Solver using " + self._solver_settings.get_heuristic_str() + \
               " heuristics minimizing " + self._solver_settings.get_objective_function()
