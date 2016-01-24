from PySide.QtGui import QLineEdit


class SelectAllLineEdit(QLineEdit):
    def focusInEvent(self, event):
        self.selectAll()
