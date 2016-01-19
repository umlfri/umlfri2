from PySide.QtGui import QLineEdit, QSpinBox


class SelectAllLineEdit(QLineEdit):
    def focusInEvent(self, event):
        self.selectAll()

class SelectAllSpinBox(QSpinBox):
    def focusInEvent(self, event):
        self.selectAll()
