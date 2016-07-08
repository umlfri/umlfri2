import os.path
from time import time

from PySide.QtCore import QTimer, Qt
from PySide.QtGui import QLabel, QPixmap, QApplication

from umlfri2.application import Application
from umlfri2.constants.paths import GRAPHICS
from umlfri2.constants.splashscreen import SPLASH_TIMEOUT


class ExitScreen(QLabel):
    def __init__(self):
        pixmap = QPixmap(os.path.join(GRAPHICS, "splash", "exit_bye.png"))
        super().__init__()
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setPixmap(pixmap)
        self.setMask(pixmap.mask())
        self.move(QApplication.desktop().screen().rect().center() - self.rect().center())

        self.__init_application()

        self.__timer = QTimer(self)
        self.__timer.timeout.connect(self.__timer_event)
        self.__timeout = time() + SPLASH_TIMEOUT / 1000
        self.__timer.start(100)
        self.__timer_event()

    def __init_application(self):
        self.__stopper = Application().addons.stop_all()

    def __timer_event(self):
        if self.__stopper.finished:
            self.__timer.stop()
            QApplication.instance().quit()
        else:
            self.__stopper.do()
    
    def closeEvent(self, event):
        event.ignore()
