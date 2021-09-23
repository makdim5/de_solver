from matplotlib import ticker
import numpy as np
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plot

from PyQt5.Qt import *
from matplotlib.patches import Polygon

MIN_X_VALUE = -100
MAX_X_VALUE = 100
AMOUNT_OF_POINTS = 1000


class PlotWidget(QWidget):
    def __init__(self, min_x=-5, max_x=5, parent=None):
        super().__init__(parent)  # Инициализируем экземпляр
        # min_x, max_x, min_y, max_y, x_step, y_step,
        self.__min_x = min_x
        self.__max_x = max_x
        self.__min_y = -5
        self.__max_y = 5
        self.__x_step = 1
        self.__y_step = 1

        self.__initUi()  # Строим интерфейс
        self.__init_graphUI()

    def __initUi(self):
        self.__mainLayout = QVBoxLayout(self)

        self.__figure = Figure()
        self.__canvas = FigureCanvas(self.__figure)
        self.__navToolbar = NavigationToolbar(self.__canvas, self)

        self.__mainLayout.addWidget(self.__canvas)
        self.__mainLayout.addWidget(self.__navToolbar)

    def __init_graphUI(self):
        self.__figure.clear()
        self.__ax = self.__figure.add_subplot(111)

        # установка делений осей
        self.__ax.xaxis.set_major_locator(ticker.MultipleLocator(self.__x_step))
        self.__ax.yaxis.set_major_locator(ticker.MultipleLocator(self.__y_step))

        self.__ax.axhline(y=0, xmin=self.__min_x, xmax=self.__max_x, color='#000000')
        self.__ax.axvline(x=0, ymin=self.__min_y, ymax=self.__max_y, color='#000000')

        self.__ax.set_ylim([self.__min_y, self.__max_y])
        self.__ax.set_xlim([self.__min_x, self.__max_x])

        self.__ax.grid()

    def clear(self):
        self.__init_graphUI()

    def plot(self, function, color='#0000FF', linestyle='-'):

        x = np.linspace(MIN_X_VALUE, MAX_X_VALUE, AMOUNT_OF_POINTS)
        y = function(x)
        self.__ax.plot(x, y, linestyle=linestyle, color=color, linewidth=3)
        self.__canvas.draw()

    def plot_from_lists(self, x_list, y_list):
        if len(x_list) == len(y_list):
            self.__ax.plot(x_list, y_list, linewidth=3)
            self.__canvas.draw()

    def change_Ox(self, a, b):
        self.__min_x = a
        self.__max_x = b
        self.__ax.set_xlim([self.__min_x, self.__max_x])
        self.__canvas.draw()

    def change_color(self, elem_num=0, color="#000000"):
        self.__figure.gca().get_lines()[elem_num].set_color(color)

    def fill_between(self, first_func, second_func, min_x, max_x, color="none",
                     hatch="\\", edgecolor="b"):
        x = np.linspace(MIN_X_VALUE, MAX_X_VALUE, AMOUNT_OF_POINTS)
        y = first_func(x)

        y2 = second_func(x)

        self.__ax.fill_between(x, y, y2, where=(x > min_x) & (x < max_x),
                               color=color, alpha=0.5,
                               hatch=hatch, edgecolor=edgecolor)

    def draw_polygon(self, x1, x2, y1, y2, color="#03d0f3"):
        list_x = [x1, x2, x2, x1]
        list_y = [0, 0, y2, y1]
        self.__ax.add_patch(Polygon(list(zip(list_x, list_y)),
                                    color=color, alpha=0.5))

        self.__canvas.draw()

    def draw_vert_line(self, val, color="#C71585"):
        self.draw_polygon(val, val, self.__min_y, self.__max_y, color=color)

    def draw_line(self, x1, y1, x2, y2, ls="-"):
        self.__ax.plot([x1, x2], [y1, y2], c='#8B2B9B', ls=ls)

    def draw_point(self, x, y):
        self.__ax.scatter([x], [y], c='g')

    def make_pause(self, s):
        plot.pause(s)

    def draw_diagram(self, function, start, end,
                     steps_amount, mode="trapezoid", color="#C71585"):
        if start > end:
            start, end = end, start

        step = (end - start) / steps_amount

        if mode == "middle":
            x = start + 0.5 * step
        elif mode == "right":
            x = start
        else:
            x = start + step

        for item in range(steps_amount):
            if mode == "trapezoid":
                self.draw_polygon(x - step, x,
                                  function(x),
                                  function(x - step), color=color)
            elif mode == "middle":
                self.draw_polygon(x - step, x,
                                  function(x),
                                  function(x), color=color)
            elif mode == "right":
                self.draw_polygon(x, x + step,
                                  function(x),
                                  function(x), color=color)
            elif mode == "left":

                self.draw_polygon(x - step, x,
                                  function(x),
                                  function(x), color=color)
            x += step
