from openpyxl import Workbook, drawing
from openpyxl.chart import ScatterChart, Reference, Series

ADD_EXCEL_NAME = r"/diffExample.xlsx"


class ExcelWorker:
    def __init__(self, way):
        self.__way = way + ADD_EXCEL_NAME
        self.__wb = Workbook()
        self.__ws = self.__wb.active
        self.__chart = ScatterChart()
        self.__chart.legend = None

    def fill_cells(self, one_list, other_list):
        for i in range(len(one_list)):
            self.__ws.append([one_list[i], other_list[i]])

    def append_info(self, info):
        self.__ws.append([info])

    def create_excel_plot(self, one_list, position="D3"):
        self.__chart.title = "Scatter Chart TEST"
        self.__chart.style = 15
        self.__chart.x_axis.title = 'X'
        self.__chart.y_axis.title = 'X^2'

        xvalues = Reference(self.__ws, min_col=1,
                            min_row=1, max_row=len(one_list))  # аргументы
        values = Reference(self.__ws, min_col=2,
                           min_row=1, max_row=len(one_list))  # значения
        series = Series(values, xvalues)  # оформдение графика
        self.__chart.series.append(series)  # добавление графика

        self.__ws.add_chart(self.__chart, position)

    def insert_image(self, image_way="test.jpg", position="C4"):
        # вставка изображения
        img = drawing.image.Image(image_way)
        img.anchor = position
        self.__ws.add_image(img)

    def save(self):
        self.__wb.save(self.__way)

    def set_way(self, way):
        self.__way = way + ADD_EXCEL_NAME
