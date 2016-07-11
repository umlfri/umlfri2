import os.path

from PySide.QtCore import QTimer, Qt
from PySide.QtGui import QLabel, QPixmap, QApplication

from umlfri2.application import Application
from umlfri2.constants.paths import GRAPHICS


class ExitScreen(QLabel):
    def __init__(self):
        super().__init__()
        
        ExitScreen.__instance = self # Needed to keep the window open
        
        self.setWindowModality(Qt.ApplicationModal)
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        pixmap = QPixmap(os.path.join(GRAPHICS, "splash", "exit_bye.png"))
        self.setPixmap(pixmap)
        self.setMask(pixmap.mask())
        self.move(QApplication.desktop().screen().rect().center() - self.rect().center())

        self.__init_application()

        self.__timer = QTimer(self)
        self.__timer.timeout.connect(self.__timer_event)
        self.__count = 0
        
    def start(self):
        self.__timer.start(100)
        self.__timer_event()

    def __init_application(self):
        self.__stopper = Application().addons.stop_all()

    def __timer_event(self):
        if self.__stopper.finished:
            self.__timer.stop()
            QApplication.instance().quit()
        else:
            if self.__count > 2:
                self.show()
            self.__count += 1
            self.__stopper.do()
    
    def closeEvent(self, event):
        event.ignore()
