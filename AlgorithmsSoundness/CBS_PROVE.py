from MAPFSolver.SearchBasedAlgorithms.AStar.AStarSolver import AStarSolver
from tkinter import *
from MAPFSolver.Utilities.Agent import Agent
from MAPFSolver.Utilities.Map import Map
from MAPFSolver.Utilities.ProblemInstance import ProblemInstance
from MAPFSolver.Utilities.SolverSettings import SolverSettings
from MAPFSolver.Utilities.problem_generation import *
from Utilities.Reader import Reader

problem_map = generate_random_map(8, 8, 0)

"""
agents = [Agent(0, (6,6), (0,4)), Agent(1, (2,0), (4,6)), Agent(2, (3,6), (4,3)), Agent(3, (0,2), (7,4)),
          Agent(6, (5,7), (0,1)), Agent(7, (4,7), (4,2))]
"""

"""
agents = [Agent(0, (6,6), (0,4)), Agent(1, (2,0), (4,6)), Agent(2, (3,6), (4,3)), Agent(3, (0,2), (7,4)),
          Agent(4, (7,2), (3,2)), Agent(5, (7,1), (6,5)), Agent(6, (5,7), (0,1)), Agent(7, (4,7), (4,2)),
          Agent(8, (7,7), (1,7))]
"""

"""
agents = [Agent(0, (6,6), (0,4)), Agent(1, (2,0), (4,6)), Agent(2, (3,6), (4,3)), Agent(3, (0,2), (7,4))]

problem_instance = ProblemInstance(problem_map, agents)
solver_settings = SolverSettings(heuristic="Manhattan", objective_function="SOC", stay_in_goal=True,
                                 goal_occupation_time=1, is_edge_conflict=True)
# solver = SolverIndependenceDetection(SolverConflictBasedSearch(solver_settings), solver_settings)
solver = AStarSolver(solver_settings)

paths, output_infos = solver.solve(problem_instance, verbose=True, return_infos=True)
print(paths)
"""
total_nodes = 0
total_time = 0
total_cost = 0


for i in range(500):
    print(i)
    agents = generate_random_agents(problem_map, 3)
    problem_instance = ProblemInstance(problem_map, agents)

    # problem_instance = generate_problem_from_map_and_scene(Reader(), 4)

    solver_settings = SolverSettings(heuristic="Manhattan", objective_function="SOC", stay_in_goal=True,
                                     goal_occupation_time=1, is_edge_conflict=True)
    # solver = SolverIndependenceDetection(SolverConflictBasedSearch(solver_settings), solver_settings)
    solver = AStarSolver(solver_settings)

    paths, output_infos = solver.solve(problem_instance, verbose=False, return_infos=True)

    total_nodes += output_infos["generated_nodes"]
    total_time += output_infos["computation_time"]
    total_cost += output_infos["sum_of_costs"]


print(total_nodes/500)
print(total_time/500)
print(total_cost/500)

"""
root = Tk()
frame = Frame(root)
frame.pack()
problem_instance.plot_on_gui(frame, paths=paths)

root.mainloop()
"""
