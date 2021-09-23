from PyQt5.QtCore import QPropertyAnimation, QEasingCurve
from PyQt5.QtWidgets import QWidget

from client.view.welcomeUI import Ui_Form


class WelcomeWin(Ui_Form, QWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.init_animation()
        self.warningMsg.hide()

    def init_animation(self):
        self.animation = QPropertyAnimation(self, b'windowOpacity')
        self.animation.setEasingCurve(QEasingCurve.InOutBounce)
        self.animation.setDuration(300)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1)
        self.animation.start()