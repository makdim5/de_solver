from PyQt5.QtWidgets import QWidget

from client.view.about import Ui_Form


class AboutWGT(Ui_Form, QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)