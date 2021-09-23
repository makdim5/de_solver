import sys

from PyQt5.QtWidgets import QApplication

from client.class_client import Client
from qt_material import apply_stylesheet

if __name__ == "__main__":
    app = QApplication(sys.argv)
    client = Client()
    apply_stylesheet(app, theme='dark_blue.xml')
    app.exec_()
    client.exit_action()

