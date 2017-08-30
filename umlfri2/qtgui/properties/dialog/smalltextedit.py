from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QTextEdit


class SmallTextEdit(QTextEdit):
    def sizeHint(self):
        return QSize(10, 10)