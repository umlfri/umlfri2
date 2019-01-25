from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QTextEdit


class EditorWidget(QTextEdit):
    text_update = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        
        self.__fire = True
        self.textChanged.connect(self.__text_changed)
        self.__timer = None
    
    def setPlainText(self, text):
        self.__fire = False
        super().setPlainText(text)
        self.__fire = True
    
    def __text_changed(self):
        if not self.__fire:
            return
        if self.__timer is not None:
            self.killTimer(self.__timer)
        self.__timer = self.startTimer(1000)
    
    def timerEvent(self, event):
        self.killTimer(self.__timer)
        self.__timer = None
        self.text_update.emit()
    
    def focusOutEvent(self, event):
        if self.__timer is not None:
            self.killTimer(self.__timer)
        self.__timer = None
        self.text_update.emit()
