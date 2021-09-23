from server.logic.diffSolvers.DiffEquationSolverBase import DiffEquationSolverBase


class DiffEquationFourSolver(DiffEquationSolverBase):
    def __init__(self, equation, interval_beg, interval_end, step):
        super().__init__(equation, interval_beg, interval_end, step)

    def F(self, x, y, y2, y3, y4, n):
        f = 0
        if n == 1:
            f = self._equation_generator(x, y, y2, y3, y4)
        elif n == 2:
            f = y2
        elif n == 3:
            f = y3
        elif n == 4:
            f = y4

        return f

    def euler_method(self, y, y2, y3, y4):
        x_s = []
        answers_euler = []
        x = self._interval_beg
        h = self._step
        while x <= self._interval_end + h:
            y1_1 = y + h * self.F(x, y, y2, y3, y4, 1)
            y1_2 = y2 + h * self.F(x, y, y2, y3, y4, 2)
            y1_3 = y3 + h * self.F(x, y, y2, y3, y4, 3)
            y1_4 = y4 + h * self.F(x, y, y2, y3, y4, 4)

            y = y1_1
            y2 = y1_2
            y3 = y1_3
            y4 = y1_4
            x_s.append(x)
            answers_euler.append(y)

            x += h
        return x_s, answers_euler

    def runge_third_method(self, y1, y2, y3, y4):
        x_s = []
        answers_runge = []
        x = self._interval_beg
        h = self._step
        while x <= self._interval_end + h:
            k1_1 = h * self.F(x, y1, y2, y3, y4, 1)
            k1_2 = h * self.F(x, y1, y2, y3, y4, 2)
            k1_3 = h * self.F(x, y1, y2, y3, y4, 3)
            k1_4 = h * self.F(x, y1, y2, y3, y4, 4)

            k2_1 = h * self.F(x + h / 2, y1 + k1_1 / 2,
                              y2 + k1_2 / 2, y3 + k1_3 / 2,
                              y4 + k1_4 / 2, 1)
            k2_2 = h * self.F(x + h / 2, y1 + k1_1 / 2,
                              y2 + k1_2 / 2, y3 + k1_3 / 2,
                              y4 + k1_4 / 2, 2)

            k2_3 = h * self.F(x + h / 2, y1 + k1_1 / 2,
                              y2 + k1_2 / 2, y3 + k1_3 / 2,
                              y4 + k1_4 / 2, 3)
            k2_4 = h * self.F(x + h / 2, y1 + k1_1 / 2,
                              y2 + k1_2 / 2, y3 + k1_3 / 2,
                              y4 + k1_4 / 2, 4)

            k3_1 = h * self.F(x + h, y1 + k2_1, y2 + k2_2,
                              y3 + k2_3, y4 + k2_4, 1)
            k3_2 = h * self.F(x + h, y1 + k2_1, y2 + k2_2,
                              y3 + k2_3, y4 + k2_4, 2)

            k3_3 = h * self.F(x + h, y1 + k2_1, y2 + k2_2,
                              y3 + k2_3, y4 + k2_4, 3)

            k3_4 = h * self.F(x + h, y1 + k2_1, y2 + k2_2,
                              y3 + k2_3, y4 + k2_4, 4)

            answers_runge.append(y1)
            x_s.append(x)
            y1 = y1 + 1 / 4 * (k1_1 + 2 * k2_1 + k3_1)
            y2 = y2 + 1 / 4 * (k1_2 + 2 * k2_2 + k3_2)
            y3 = y3 + 1 / 4 * (k1_3 + 2 * k2_3 + k3_3)
            y4 = y4 + 1 / 4 * (k1_4 + 2 * k2_4 + k3_4)
            x += h

        return x_s, answers_runge

    def runge_forth_method(self, y1, y2, y3, y4):
        x_s = []
        answers_runge = []
        x = self._interval_beg
        h = self._step
        while x <= self._interval_end + h:
            k1_1 = h * self.F(x, y1, y2, y3, y4, 1)
            k1_2 = h * self.F(x, y1, y2, y3, y4, 2)
            k1_3 = h * self.F(x, y1, y2, y3, y4, 3)
            k1_4 = h * self.F(x, y1, y2, y3, y4, 4)

            k2_1 = h * self.F(x + h / 2, y1 + k1_1 / 2, y2 + k1_2 / 2,
                              y3 + k1_3 / 2, y3 + k1_4, 1)
            k2_2 = h * self.F(x + h / 2, y1 + k1_1 / 2, y2 + k1_2 / 2,
                              y3 + k1_3 / 2, y3 + k1_4, 2)
            k2_3 = h * self.F(x + h / 2, y1 + k1_1 / 2, y2 + k1_2 / 2,
                              y3 + k1_3 / 2, y3 + k1_4, 3)
            k2_4 = h * self.F(x + h / 2, y1 + k1_1 / 2, y2 + k1_2 / 2,
                              y3 + k1_3 / 2, y3 + k1_4, 4)

            k3_1 = h * self.F(x + h / 2, y1 + k2_1 / 2, y2 + k2_2 / 2,
                              y3 + k2_3 / 2, y4 + k2_4 / 2, 1)
            k3_2 = h * self.F(x + h / 2, y1 + k2_1 / 2, y2 + k2_2 / 2,
                              y3 + k2_3 / 2, y4 + k2_4 / 2, 2)
            k3_3 = h * self.F(x + h / 2, y1 + k2_1 / 2, y2 + k2_2 / 2,
                              y3 + k2_3 / 2, y4 + k2_4 / 2, 3)
            k3_4 = h * self.F(x + h / 2, y1 + k2_1 / 2, y2 + k2_2 / 2,
                              y3 + k2_3 / 2, y4 + k2_4 / 2, 4)

            k4_1 = h * self.F(x + h, y1 + k3_1, y2 + k3_2,
                              y3 + k3_3, y4 + k3_4, 1)
            k4_2 = h * self.F(x + h, y1 + k3_1, y2 + k3_2,
                              y3 + k3_3, y4 + k3_4, 2)
            k4_3 = h * self.F(x + h, y1 + k3_1, y2 + k3_2,
                              y3 + k3_3, y4 + k3_4, 3)
            k4_4 = h * self.F(x + h, y1 + k3_1, y2 + k3_2,
                              y3 + k3_3, y4 + k3_4, 4)

            answers_runge.append(y1)
            x_s.append(x)
            y1 = y1 + 1 / 6 * (k1_1 + 2 * k2_1 + 2 * k3_1 + k4_1)
            y2 = y2 + 1 / 6 * (k1_2 + 2 * k2_2 + 2 * k3_2 + k4_2)
            y3 = y3 + 1 / 6 * (k1_3 + 2 * k2_3 + 2 * k3_3 + k4_3)
            y4 = y4 + 1 / 6 * (k1_4 + 2 * k2_4 + 2 * k3_4 + k4_4)
            x += h

        return x_s, answers_runge
