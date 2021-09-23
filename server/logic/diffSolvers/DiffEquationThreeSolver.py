from server.logic.diffSolvers.DiffEquationSolverBase import DiffEquationSolverBase


class DiffEquationThreeSolver(DiffEquationSolverBase):
    def __init__(self, equation, interval_beg, interval_end, step):
        super().__init__(equation, interval_beg, interval_end, step)

    def F(self, x, y, y2, y3, n):
        f = 0
        if n == 1:
            f = self._equation_generator(x, y, y2, y3)
        elif n == 2:
            f = y2
        elif n == 3:
            f = y3

        return f

    def euler_method(self, y, y2, y3):
        x_s = []
        answers_euler = []
        x = self._interval_beg
        h = self._step
        while x <= self._interval_end + h:
            y1_1 = y + h * self.F(x, y, y2, y3, 1)
            y1_2 = y2 + h * self.F(x, y, y2, y3, 2)
            y1_3 = y3 + h * self.F(x, y, y2, y3, 3)

            y = y1_1
            y2 = y1_2
            y3 = y1_3
            x_s.append(x)
            answers_euler.append(y)

            x += h
        return x_s, answers_euler

    def runge_third_method(self, y, y2, y3):
        x_s = []
        answers_runge = []
        x = self._interval_beg
        h = self._step
        while x <= self._interval_end + h:
            k1_1 = h * self.F(x, y, y2, y3, 1)
            k1_2 = h * self.F(x, y, y2, y3, 2)
            k1_3 = h * self.F(x, y, y2, y3, 3)

            k2_1 = h * self.F(x + h / 2, y + k1_1 / 2,
                              y2 + k1_2 / 2, y3 + k1_3 / 2, 1)
            k2_2 = h * self.F(x + h / 2, y + k1_1 / 2, y2 + k1_2 / 2,
                              y3 + k1_3 / 2, 2)

            k2_3 = h * self.F(x + h / 2, y + k1_1 / 2, y2 + k1_2 / 2,
                              y3 + k1_3 / 2, 3)

            k3_1 = h * self.F(x + h, y + k2_1, y2 + k2_2,
                              y3 + k2_3, 1)
            k3_2 = h * self.F(x + h, y + k2_1, y2 + k2_2,
                              y3 + k2_3, 2)

            k3_3 = h * self.F(x + h, y + k2_1, y2 + k2_2,
                              y3 + k2_3, 3)

            answers_runge.append(y)
            x_s.append(x)
            y = y + 1 / 4 * (k1_1 + 2 * k2_1 + k3_1)
            y2 = y2 + 1 / 4 * (k1_2 + 2 * k2_2 + k3_2)
            y3 = y3 + 1 / 4 * (k1_3 + 2 * k2_3 + k3_3)
            x += h

        return x_s, answers_runge

    def runge_forth_method(self, y, y2, y3):
        x_s = []
        answers_runge = []
        x = self._interval_beg
        h = self._step
        while x <= self._interval_end + h:
            k1_1 = h * self.F(x, y, y2, y3, 1)
            k1_2 = h * self.F(x, y, y2, y3, 2)
            k1_3 = h * self.F(x, y, y2, y3, 3)

            k2_1 = h * self.F(x + h / 2, y + k1_1 / 2, y2 + k1_2 / 2,
                                                 y3 + k1_3 / 2, 1)
            k2_2 = h * self.F(x + h / 2, y + k1_1 / 2, y2 + k1_2 / 2,
                                                 y3 + k1_3 / 2, 2)

            k2_3 = h * self.F(x + h / 2, y + k1_1 / 2, y2 + k1_2 / 2,
                                                 y3 + k1_3 / 2, 3)

            k3_1 = h * self.F(x + h / 2, y + k2_1 / 2, y2 + k2_2 / 2,
                                                 y3 + k2_3 / 2, 1)
            k3_2 = h * self.F(x + h / 2, y + k2_1 / 2, y2 + k2_2 / 2,
                                                 y3 + k2_3 / 2, 2)
            k3_3 = h * self.F(x + h / 2, y + k2_1 / 2, y2 + k2_2 / 2,
                                                 y3 + k2_3 / 2, 3)

            k4_1 = h * self.F(x + h, y + k3_1, y2 + k3_2,
                                                 y3 + k3_3, 1)
            k4_2 = h * self.F(x + h, y + k3_1, y2 + k3_2,
                                                 y3 + k3_3, 2)
            k4_3 = h * self.F(x + h, y + k3_1, y2 + k3_2,
                                                 y3 + k3_3, 3)

            answers_runge.append(y)
            x_s.append(x)
            y = y + 1 / 6 * (k1_1 + 2 * k2_1 + 2 * k3_1 + k4_1)
            y2 = y2 + 1 / 6 * (k1_2 + 2 * k2_2 + 2 * k3_2 + k4_2)
            y3 = y3 + 1 / 6 * (k1_3 + 2 * k2_3 + 2 * k3_3 + k4_3)
            x += h

        return x_s, answers_runge
