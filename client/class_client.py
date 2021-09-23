import os
import socket

from client.view.DE_Solver_window import DiffEquationSolverWindow

from client.view.welcomeWin import WelcomeWin

from util import *
from util.NumberArrayWorker import NumberArrayWorker
from util.StrArrayWorker import StrArrayWorker

SERVER_ADDRESS = "127.0.0.1"
PORT = 11000
BYTES_PER_PACKAGE = 100000


class Client:
    def __init__(self):
        self.client = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )
        self.app = DiffEquationSolverWindow()
        self.app.action.triggered.connect(lambda : os.system("help.chm"))

        self.server_dns_name = ""  # HP-PYMAK
        self.welcome_win = WelcomeWin()
        self.welcome_win.show()
        self.welcome_win.pushButton.clicked.connect(self.welcome_commands)
        self.welcome_win.lineEdit.returnPressed.connect(self.welcome_commands)

        self.app.result_btn.clicked.connect(self.solve_equation_action)

    def welcome_commands(self):
        try:
            self.server_dns_name = self.welcome_win.lineEdit.text()
            self.connect()
            self.welcome_win.close()
            self.app.show()
        except Exception:
            self.welcome_win.warningMsg.show()
            self.welcome_win.lineEdit.clear()

    def connect(self):
        self.client.connect(
            (self.server_dns_name, PORT)
        )

    def send(self, msg):
        self.client.send(msg.encode("utf-8"))

    def receive(self):
        return self.client.recv(BYTES_PER_PACKAGE).decode("utf-8")

    def solve_equation_action(self):
        self.send(SOLVE_DIFF)
        self.send(StrArrayWorker.convert_list_str_to_string(
            self.app.get_general_info()))

        info = self.receive()
        if "Error" not in info:
            x_array = NumberArrayWorker.convert_string_to_list_number(info)
            y_array = NumberArrayWorker.convert_string_to_list_number(self.receive())

            self.app.show_solution(x_array, y_array)
        else:
            self.app.msgBox.setText(info)
            self.app.msgBox.show()

    def exit_action(self):
        self.send(EXIT)
