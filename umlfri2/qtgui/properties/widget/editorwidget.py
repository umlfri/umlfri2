from PyQt5.QtCore import pyqtSignal, QTimer
from PyQt5.QtWidgets import QTextEdit


class EditorWidget(QTextEdit):
    text_update = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        
        self.__timer = QTimer(self)
        self.__timer.setSingleShot(True)
        self.__timer.setInterval(1000)
        self.__timer.timeout.connect(self.__time_out)
        self.__fire = True
        self.textChanged.connect(self.__text_changed)
    
    def setPlainText(self, text):
        self.__fire = False
        super().setPlainText(text)
        self.__fire = True
    
    def __text_changed(self):
        if not self.__fire:
            return
        self.__timer.stop()
        self.__timer.start()
    
    def __time_out(self):
        self.text_update.emit()
    
    def focusOutEvent(self, event):
        self.__timer.stop()
        self.text_update.emit()
