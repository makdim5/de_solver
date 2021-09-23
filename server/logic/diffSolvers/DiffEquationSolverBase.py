import keyword
import re

from server.logic.exceptions.ExpressionMistakeException import ExpressionMistakeException
from server.logic.exceptions.ImpossibleExpressionException import ImpossibleExpressionException


# def controller(expression, a, b, step, mode, method, y, y2=0, y3=0, y4=0):


class DiffEquationSolverBase:
    def __init__(self, equation, interval_beg, interval_end, step):

        self._interval_beg = interval_beg
        self._interval_end = interval_end
        self._step = step

        self._equation = self._reformat_expression(equation)

        if not self._is_right_expression(self._equation):
            raise ImpossibleExpressionException()

    @staticmethod
    def _reformat_expression(expression):
        expression = re.sub("y'''", "y4", expression)
        expression = re.sub("y''", "y3", expression)

        return re.sub("y'", "y2", expression)

    @staticmethod
    def _is_right_expression(expression):
        if expression == "":
            return False
        impossible_words = keyword.kwlist

        impossible_words += [",", "print", "exec", "eval"]
        for item in impossible_words:
            temp = re.findall(item, expression)
            if len(temp) != 0:
                return False

        return True

    def _equation_generator(self, x=0, y=0, y2=0, y3=0, y4=0):
        fns = '''def function(x, y, y2, y3, y4):
        from math import sin, cos, tan, log, exp, sqrt, fabs
        return ''' + self._equation
        try:
            exec(fns)
            result = eval('function(' + str(x) + ',' + str(y) + ',' +
                          str(y2) + ',' + str(y3) + ',' + str(y4) + ')')
        except SyntaxError:
            raise ExpressionMistakeException()
        return result

    def get_equation(self):
        return self._equation

    def set_equation(self, equation):
        self._equation = self._reformat_expression(equation)
        if not self._is_right_expression(self._equation):
            raise ImpossibleExpressionException

    def get_interval_beg(self):
        return self._interval_beg

    def set_interval_beg(self, interval_beg):
        self._interval_beg = interval_beg

    def get_interval_end(self):
        return self._interval_end

    def set_interval_end(self, interval_end):
        self._interval_end = interval_end

    def get_step(self):
        return self._step

    def set_step(self, step):
        self._step = step
