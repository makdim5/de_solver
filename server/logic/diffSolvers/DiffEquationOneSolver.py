from server.logic.diffSolvers.DiffEquationSolverBase import DiffEquationSolverBase


class DiffEquationOneSolver(DiffEquationSolverBase):
    def __init__(self, equation, interval_beg, interval_end, step):
        super().__init__(equation, interval_beg, interval_end, step)

    def F(self, x, y):

        return self._equation_generator(x, y)

    def euler_method(self, y):
        x_s = []
        answers_euler = []
        x = self._interval_beg
        h = self._step
        while x <= self._interval_end + h:
            y1_1 = y + h * self.F(x, y)
            y = y1_1

            x_s.append(x)
            answers_euler.append(y)

            x += h
        return x_s, answers_euler

    def runge_third_method(self, y):
        x_s = []
        answers_runge = []
        x = self._interval_beg
        h = self._step
        while x <= self._interval_end + h:
            k1_1 = h * self.F(x, y)

            k2_1 = h * self.F(x + h / 2, y + k1_1 / 2)

            k3_1 = h * self.F(x + h, y + k2_1)

            answers_runge.append(y)
            x_s.append(x)
            y = y + 1 / 4 * (k1_1 + 2 * k2_1 + k3_1)
            x += h

        return x_s, answers_runge

    def runge_forth_method(self, y):
        x_s = []
        answers_runge = []
        x = self._interval_beg
        h = self._step
        while x <= self._interval_end + h:
            k1_1 = h * self.F(x, y)
            k2_1 = h * self.F(x + h / 2, y + k1_1 / 2)
            k3_1 = h * self.F(x + h / 2, y + k2_1 / 2)
            k4_1 = h * self.F(x + h, y + k3_1)

            answers_runge.append(y)
            x_s.append(x)
            y = y + 1 / 6 * (k1_1 + 2 * k2_1 + 2 * k3_1 + k4_1)
            x += h

        return x_s, answers_runge
