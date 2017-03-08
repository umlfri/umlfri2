from PyQt5.QtWidgets import QLineEdit


class SelectAllLineEdit(QLineEdit):
    def focusInEvent(self, event):
        self.selectAll()
