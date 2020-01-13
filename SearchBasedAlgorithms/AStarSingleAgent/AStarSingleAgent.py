"""
A* single agent solver. It computes the path for each agent without considering any conflict.
"""
from Utilities.MAPFSolver import MAPFSolver
from Utilities.AStar import AStar
import time


class AStarSingleAgent(MAPFSolver):
    def __init__(self, solver_settings, objective_function):
        super().__init__(solver_settings, objective_function)

    def solve(self, problem_instance, verbose=False, print_output=True, return_infos=False):
        """
        Solve the MAPF problem using the A* algorithm individually for each agent, without considering any conflict.
        It returns the paths as lists of list of (x, y) positions.
        """
        start = time.time()

        paths = []
        for agent in problem_instance.get_agents():
            a_star = AStar(self._solver_settings)
            path = a_star.find_path(problem_instance.get_map(), agent.get_start(), agent.get_goal())
            paths.append(path)
        if print_output:
            print("Total time: ", max([len(path)-1 for path in paths]),
                  " Total cost:", sum([len(path)-self._solver_settings.get_goal_occupation_time() for path in paths]))

        if return_infos:
            output_infos = {
                "sum_of_costs": sum([len(path)-self._solver_settings.get_goal_occupation_time() for path in paths]),
                "makespan": max([len(path)-1 for path in paths]),
                "expanded_nodes": 0,
                "computation_time": time.time() - start
            }
            return paths, output_infos

        return paths

    def __str__(self):
        return "A* Single Agent Solver using " + self._solver_settings.get_heuristics_str() + " heuristics"