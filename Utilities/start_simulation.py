from SearchBasedAlgorithms.AStarMultiAgent.SolverAStarMultiAgent import SolverAStarMultiAgent
from SearchBasedAlgorithms.AStarMultiAgent.SolverAStarOD import SolverAStarOD
from SearchBasedAlgorithms.CooperativeAStar.SolverCooperativeAStar import SolverCooperativeAStar
from SearchBasedAlgorithms.ConflictBasedSearch.SolverConflictBasedSearch import SolverConflictBasedSearch
from SearchBasedAlgorithms.IndependenceDetection.SolverIndependenceDetection import SolverIndependenceDetection
from SearchBasedAlgorithms.IncreasingCostTreeSearch.SolverIncreasingCostTreeSearch import SolverIncreasingCostTreeSearch
from SearchBasedAlgorithms.MStar.SolverMStar import SolverMStar
from Utilities.read_map_and_scenario import *
from Utilities.ProblemInstance import *
from Utilities.Agent import *
from Utilities.Map import *


def prepare_simulation(frame, algorithm, independence_detection, map_number, solver_settings, obj_function, n_of_agents):
    """
    Solve the MAPF problem and visualize the simulation on the frame.
    :param frame: Frame where the simulation will be displayed
    :param algorithm: String of the algorithm choose
    :param independence_detection: True if Independence Detection will be used with the algorithm
    :param map_number: Number of the map choose
    :param solver_settings: Settings of the solver (heuristics, goal_occupation_time)
    :param obj_function: Objective function used
    :param n_of_agents: Number of Agents on the map
    """
    map = get_map(map_number)
    agents = get_agents(map_number, map, n_of_agents)
    problem_instance = ProblemInstance(map, agents)

    solver = get_solver(algorithm, solver_settings, obj_function, independence_detection)
    print("Solver --> ", solver, "\nSolving...")
    paths, output_infos = solver.solve(problem_instance, verbose=True, return_infos=True)
    print("Solved.")

    problem_instance.plot_on_gui(frame, paths, output_infos)


def get_solver(algorithm, solver_settings, objective_function, independence_detection):
    """
    Return the Solver object for the specified algorithm and relative settings.
    """
    switcher = {
        "Cooperative A*": SolverCooperativeAStar(solver_settings, objective_function),
        "A*": SolverAStarMultiAgent(solver_settings, objective_function),
        "A* with Operator Decomposition": SolverAStarOD(solver_settings, objective_function),
        "Increasing Cost Tree Search": SolverIncreasingCostTreeSearch(solver_settings, objective_function),
        "Conflict Based Search": SolverConflictBasedSearch(solver_settings, objective_function),
        "M*": SolverMStar(solver_settings, objective_function)
    }
    if independence_detection:
        return SolverIndependenceDetection(switcher.get(algorithm), solver_settings, objective_function)
    else:
        return switcher.get(algorithm)


def get_map(map_number):
    """
    Return the map object given the number of the choosen map.
    """
    print("Loading map...")
    map_width, map_height, occupancy_list = load_map_file(MAPS_LIST.get(map_number))
    print("Map loaded.")

    return Map(map_height, map_width, occupancy_list)


def get_agents(scene_number, map, n_of_agents):
    """
    Return the Agent list for the specified scene number of the given map and the selected number of agents.
    """
    print("Loading scenario file...")
    agents = load_scenario_file(SCENES_LIST.get(scene_number), map.get_obstacles_xy(), map.get_width(),
                                map.get_height(), number_of_agents=n_of_agents)
    print("Scenario loaded.")

    return [Agent(i, a[0], a[1]) for i, a in enumerate(agents)]

