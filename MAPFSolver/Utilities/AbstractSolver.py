import abc


class MAPFSolver:
    """
    Abstract class for any solver.
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self, solver_settings):
        self._solver_settings = solver_settings

    @abc.abstractmethod
    def solve(self, problem_instance, verbose=False, return_infos=False):
        """
        Compute the paths.
        :param problem_instance: instance of the problem to solve.
        :param verbose: if True, infos will be printed on terminal.
        :param return_infos: if True in addition to the paths will be returned also a structure with output infos.
        """

    @staticmethod
    def generate_output_infos(soc, makespan, generated_nodes, expanded_nodes, computation_time):
        """
        Return a struct with the output infos.
        """
        return {
            "sum_of_costs": soc,
            "makespan": makespan,
            "generated_nodes": generated_nodes,
            "expanded_nodes": expanded_nodes,
            "computation_time": computation_time
        }