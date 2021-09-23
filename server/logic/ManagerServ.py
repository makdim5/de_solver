from server import logic
from server.logic.diffSolvers.DiffEquationOneSolver import DiffEquationOneSolver as OneSolver
from server.logic.diffSolvers.DiffEquationTwoSolver import DiffEquationTwoSolver as TwoSolver
from server.logic.diffSolvers.DiffEquationThreeSolver import DiffEquationThreeSolver as ThreeSolver
from server.logic.diffSolvers.DiffEquationFourSolver import DiffEquationFourSolver as FourSolver

EPS = 5


class ManagerServ:
    @staticmethod
    def solve_equation(info):

        """     Info structure:
                [DIFF_EQUATION_TYPE, EQUATION, METHOD, INTERVAL_BEG, INTERVAL_END,
                STEP, Y, Y', Y'', Y''']
                """

        diff_eq_type = info[0]
        equation = info[1]
        method = info[2]

        a = float(info[3])
        b = float(info[4])

        step = float(info[5])

        y = float(info[6])
        d_y = float(info[7])

        dd_y = float(info[8])
        ddd_y = float(info[9])

        x_data = []
        y_data = []

        if diff_eq_type == logic.diffSolvers.DIFF_EQUATION_TYPE_TWO:
            solver = TwoSolver(equation, a, b, step)

            if method == logic.diffSolvers.EULER_METHOD:
                x_data, y_data = solver.euler_method(y, d_y)
            elif method == logic.diffSolvers.RUNGE_THIRD_METHOD:
                x_data, y_data = solver.runge_third_method(y, d_y)
            elif method == logic.diffSolvers.RUNGE_FOURTH_METHOD:
                x_data, y_data = solver.runge_forth_method(y, d_y)

        elif diff_eq_type == logic.diffSolvers.DIFF_EQUATION_TYPE_THREE:
            solver = ThreeSolver(equation, a, b, step)

            if method == logic.diffSolvers.EULER_METHOD:
                x_data, y_data = solver.euler_method(y, d_y, dd_y)
            elif method == logic.diffSolvers.RUNGE_THIRD_METHOD:
                x_data, y_data = solver.runge_third_method(y, d_y, dd_y)
            elif method == logic.diffSolvers.RUNGE_FOURTH_METHOD:
                x_data, y_data = solver.runge_forth_method(y, d_y, dd_y)

        elif diff_eq_type == logic.diffSolvers.DIFF_EQUATION_TYPE_FOUR:
            solver = FourSolver(equation, a, b, step)

            if method == logic.diffSolvers.EULER_METHOD:
                x_data, y_data = solver.euler_method(y, d_y, dd_y, ddd_y)
            elif method == logic.diffSolvers.RUNGE_THIRD_METHOD:
                x_data, y_data = solver.runge_third_method(y, d_y, dd_y, ddd_y)
            elif method == logic.diffSolvers.RUNGE_FOURTH_METHOD:
                x_data, y_data = solver.runge_forth_method(y, d_y, dd_y, ddd_y)

        elif diff_eq_type == logic.diffSolvers.DIFF_EQUATION_TYPE_ONE:
            solver = OneSolver(equation, a, b, step)
            if method == logic.diffSolvers.EULER_METHOD:
                x_data, y_data = solver.euler_method(y)
            elif method == logic.diffSolvers.RUNGE_THIRD_METHOD:
                x_data, y_data = solver.runge_third_method(y)
            elif method == logic.diffSolvers.RUNGE_FOURTH_METHOD:
                x_data, y_data = solver.runge_forth_method(y)

        return x_data, y_data

