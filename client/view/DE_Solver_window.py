
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QAction, QFileDialog, QMessageBox

from client.view.design_DE_Solver import Ui_MainWindow
from client.view.images.aboutWGT import AboutWGT
from client.view.plotWidget import PlotWidget

from util import *
from util.OfficeWork.excel import ExcelWorker
from util.OfficeWork.powerpoint_ex import PowerPointWorker
from util.OfficeWork.word import WordWorker


class DiffEquationSolverWindow(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.__graph = PlotWidget()
        self.graph_lay.addWidget(self.__graph)

        self.msgBox = QMessageBox()

        self.__aboutWGT = AboutWGT()
        self.toolbar = self.addToolBar("")
        self.toolbar.setMovable(False)

        self.d_y_frame.hide()
        self.dd_y_frame.hide()
        self.ddd_y_frame.hide()
        self.y_label.setText("y(" + str(self.low_val.value()) + ") = ")

        self.comboBox.currentIndexChanged.connect(self.__comboBox_actions)

        self.low_val.valueChanged.connect(self.make_low_box_actions)
        self.high_val.valueChanged.connect(self.make_high_box_actions)

        self.menu_actions()

    def menu_actions(self):
        self.action_2.triggered.connect(self.__aboutWGT.show)
        self.action_2.setText("О программе")
        self.action_2.setIcon(QIcon(r"client\view\images\info.png"))
        self.toolbar.addAction(self.action_2)

        setts_hide_action = QAction(
            QIcon(r"client\view\images\setts.png"),
            "Спрятать\Открыть меню для уравнений", self)

        setts_hide_action.triggered.connect(self.hide_open_setts_menu)

        self.toolbar.addAction(setts_hide_action)

        self.action_Word.setIcon(QIcon(r"client\view\images\word.png"))
        self.action_Word.setText("Экспорт в Word")
        self.action_Word.triggered.connect(self.to_word)

        self.action_Excel.setIcon(QIcon(r"client\view\images\Xcel.png"))
        self.action_Excel.setText("Экспорт в Excel")
        self.action_Excel.triggered.connect(self.to_excel)

        self.action_PowerPoint.setIcon(QIcon(r"client\view\images\pptx.png"))
        self.action_PowerPoint.setText("Экспорт в PowerPoint")
        self.action_PowerPoint.triggered.connect(self.to_pptx)

        self.action.setText("Открыть систему помощи")
        self.action.setIcon(QIcon(r"client\view\images\help.png"))

        self.toolbar.addAction(self.action_Word)
        self.toolbar.addAction(self.action_Excel)
        self.toolbar.addAction(self.action_PowerPoint)
        self.toolbar.addAction(self.action)

    def hide_open_setts_menu(self):
        if self.setts_frame.maximumWidth() == 250:
            self.setts_frame.setMaximumWidth(0)
        elif self.setts_frame.maximumWidth() == 0:
            self.setts_frame.setMaximumWidth(250)

    def make_low_box_actions(self):
        self.__graph.change_Ox(self.low_val.value(), self.high_val.value())
        self.y_label.setText("y(" + str(self.y_spin.value()) + ")=")

    def make_high_box_actions(self):
        self.__graph.change_Ox(self.low_val.value(), self.high_val.value())

    def show_solution(self, x, y):
        self.__graph.clear()
        self.__graph.plot_from_lists(x, y)
        self.__table_actions(x, y)

        self.msgBox.setText("Решение найдено!!!")
        self.msgBox.show()

    def __comboBox_actions(self):
        self.d_y_frame.hide()
        self.dd_y_frame.hide()
        self.ddd_y_frame.hide()

        self.y_spin.clear()
        self.d_y_spin.clear()
        self.dd_y_spin.clear()
        self.ddd_y_spin.clear()
        if self.comboBox.currentIndex() == 0:
            self.diffLabel.setText("y' = ")

            self.y_label.setText("y(" + str(self.low_val.value()) + ") = ")

        elif self.comboBox.currentIndex() == 1:
            self.diffLabel.setText("y'' = ")
            self.d_y_frame.show()

            self.y_label.setText("y(" + str(self.low_val.value()) + ") = ")
            self.d_y_label.setText("y'(" + str(self.low_val.value()) + ") = ")

        elif self.comboBox.currentIndex() == 2:
            self.diffLabel.setText("y''' = ")
            self.d_y_frame.show()
            self.dd_y_frame.show()

            self.y_label.setText("y(" + str(self.low_val.value()) + ") = ")
            self.d_y_label.setText("y'(" + str(self.low_val.value()) + ") = ")
            self.dd_y_label.setText("y''(" + str(self.low_val.value()) + ") = ")

        elif self.comboBox.currentIndex() == 3:
            self.diffLabel.setText("y'''' = ")
            self.d_y_frame.show()
            self.dd_y_frame.show()
            self.ddd_y_frame.show()

            self.y_label.setText("y(" + str(self.low_val.value()) + ") = ")
            self.d_y_label.setText("y'(" + str(self.low_val.value()) + ") = ")
            self.dd_y_label.setText("y''(" + str(self.low_val.value()) + ") = ")
            self.ddd_y_label.setText("y'''(" + str(self.low_val.value()) + ") = ")

    def __table_actions(self, x, y):
        self.tableWidget.setColumnCount(len(x))
        self.tableWidget.resizeColumnsToContents()

        if len(x) != len(y):
            return

        for i in range(len(x)):
            self.tableWidget.setColumnWidth(i, 90)
            self.tableWidget.setItem(0, i, QTableWidgetItem(str(round(x[i], 3))))
            if isinstance(y[i], complex):
                self.tableWidget.setItem(1, i, QTableWidgetItem(str(round(y[i].real, 3))))
            elif isinstance(y[i], float):
                self.tableWidget.setItem(1, i, QTableWidgetItem(str(round(y[i], 3))))

    def get_general_info(self):
        """
        Info structure:
        [DIFF_EQUATION_TYPE, EQUATION, METHOD, INTERVAL_BEG, INTERVAL_END,
        STEP, Y, Y', Y'', Y''']
        """
        info = []

        if self.comboBox.currentIndex() == 0:
            info.append(DIFF_EQUATION_TYPE_ONE)
        elif self.comboBox.currentIndex() == 1:
            info.append(DIFF_EQUATION_TYPE_TWO)
        elif self.comboBox.currentIndex() == 2:
            info.append(DIFF_EQUATION_TYPE_THREE)
        elif self.comboBox.currentIndex() == 3:
            info.append(DIFF_EQUATION_TYPE_FOUR)

        info.append(self.equationLine.text())

        info.append(EULER_METHOD)

        if self.radioButton_3.isChecked():
            info[2] = RUNGE_THIRD_METHOD

        elif self.radioButton_4.isChecked():
            info[2] = RUNGE_FOURTH_METHOD

        info.append(str(self.low_val.value()))
        info.append(str(self.high_val.value()))
        info.append(str(self.stepSpin.value()))

        info.append(str(self.y_spin.value()))
        info.append(str(self.d_y_spin.value()))
        info.append(str(self.dd_y_spin.value()))
        info.append(str(self.ddd_y_spin.value()))

        return info

    def get_general_info_for_presentation_in_office(self):
        result = ("Уравнение: " + self.diffLabel.text() +
                  self.equationLine.text())

        result += "\nТип уравнения: "

        if self.comboBox.currentIndex() == 0:
            result += "первого порядка "
            result += ("\nНачальные условия: " + self.y_label.text()
                       + str(self.y_spin.value()) + "\n")
        elif self.comboBox.currentIndex() == 1:
            result += "второго порядка "
            result += ("\nНачальные условия: " + self.y_label.text()
                       + str(self.y_spin.value()) + " " +
                       self.d_y_label.text()
                       + str(self.d_y_spin.value()) +
                       "\n")
        elif self.comboBox.currentIndex() == 2:
            result += "третьего порядка "
            result += ("\nНачальные условия: " + self.y_label.text()
                       + str(self.y_spin.value()) + " " +
                       self.d_y_label.text()
                       + str(self.d_y_spin.value()) + " " +
                       self.dd_y_label.text()
                       + str(self.dd_y_spin.value()) +
                       "\n")
        elif self.comboBox.currentIndex() == 3:
            result += "четвертого порядка "
            result += ("\nНачальные условия: " + self.y_label.text()
                       + str(self.y_spin.value()) + " " +
                       self.d_y_label.text()
                       + str(self.d_y_spin.value()) + " " +
                       self.dd_y_label.text()
                       + str(self.dd_y_spin.value()) + " " +
                       self.ddd_y_label.text()
                       + str(self.ddd_y_spin.value()) +
                       "\n")

        result += "\nМетод решения: "

        method = "Эйлера"
        if self.radioButton_3.isChecked():
            method = "Рунге-Кутта 3-го порядка"

        elif self.radioButton_4.isChecked():
            method = "Рунге-Кутта 4-го порядка"

        result += method

        result += ("\nПромежуток: [" + str(self.low_val.value()) +
                   ", " + str(self.high_val.value()) + "]")

        result += "\nШаг: " + str(self.stepSpin.value()) + "\n"

        return result

    def to_word(self):
        file_way = QFileDialog.getExistingDirectory(self, "Выбрать папку", ".")
        word_worker = WordWorker(file_way)
        p = self.grab()
        p.save("test.jpg")

        word_worker.insert_info(self.get_general_info_for_presentation_in_office(),
                                "test.jpg")

        word_worker.save()

        self.msgBox.setText("Экспортировано в Word по пути\n" + file_way)
        self.msgBox.show()

    def to_excel(self):
        file_way = QFileDialog.getExistingDirectory(self, "Выбрать папку", ".")
        excel_worker = ExcelWorker(file_way)
        excel_worker.append_info(self.get_general_info_for_presentation_in_office())
        p = self.grab()
        p.save("test.jpg")
        excel_worker.insert_image("test.jpg", position="E1")

        excel_worker.save()

        self.msgBox.setText("Экспортировано в Excel по пути\n" + file_way)
        self.msgBox.show()

    def to_pptx(self):
        file_way = QFileDialog.getExistingDirectory(self, "Выбрать папку", ".")
        pptx_worker = PowerPointWorker(file_way)
        p = self.grab()
        p.save("test.jpg")

        pptx_worker.insert_info(self.get_general_info_for_presentation_in_office(),
                                "test.jpg")

        pptx_worker.save()

        self.msgBox.setText("Экспортировано в PowerPoint по пути\n" + file_way)
        self.msgBox.show()


