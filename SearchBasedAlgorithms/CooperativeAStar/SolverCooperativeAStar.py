"""
Cooperative A* (CA*) is a an algorithm for solving the Co-operative Path-finding problem.
The task is decoupled into a series of single agent searches. The individual searches
are performed in three dimensional space-time, and take account of the planned routes of other agents.
A wait move is included in the agent’s action set, to enable it to remain stationary.
After each agent’s route is calculated, the states along the route are marked into a reservation table.
Entries in the reservation table are considered impassable and are avoided during searches by subsequent agents.
The reservation table represents the agents’ shared knowledge about each other’s planned routes.
It is a sparse data structure marking off regions of space-time.
A simple implementation, used here, is to treat the reservation table as a 3-dimensional grid (two spatial dimensions
and one time dimension). Each cell of the grid that is intersected by the agent’s planned route is marked as impassable
for precisely the duration of the intersection, thus preventing any other agent from planning a colliding route. Only a
small proportion of grid locations will be touched, and so the grid can be efficiently implemented as a hash table,
hashing on a randomly distributed function of the (x, y, t) key.
"""
from Utilities.MAPFSolver import MAPFSolver
from Utilities.AStar import AStar
from Utilities.macros import *


class SolverCooperativeAStar(MAPFSolver):
    """
    With RRA as heuristics it became HierarchicalCooperativeA*
    """
    def __init__(self, heuristics_str):
        super().__init__(heuristics_str)
        self._reservation_table = None

    def solve(self, problem_instance, verbose=False, print_output=True):
        """
        Solve the MAPF problem using the Cooperative A* algorithm returning the paths as lists of list of (x, y)
        positions.
        """
        self._reservation_table = dict()
        paths = []

        for i, agent in enumerate(problem_instance.get_agents()):
            if verbose:
                print("Agent n:", i+1, "of", len(problem_instance.get_agents()))

            solver = AStar(self._heuristics_str)
            path = solver.find_path_with_reservation_table(problem_instance.get_map(), agent.get_start(),
                                                           agent.get_goal(), self._reservation_table)
            paths.append(path)

            for j, pos in enumerate(path):
                if not self._reservation_table.get(pos):
                    self._reservation_table[pos] = []
                self._reservation_table[pos].append(j)

        if print_output:
            print("Total time: ", max([len(path)-1 for path in paths]),
                  " Total cost:", sum([len(path)-GOAL_OCCUPATION_TIME for path in paths]))
        return paths