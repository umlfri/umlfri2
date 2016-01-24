from PySide.QtGui import QSpinBox


class SelectAllSpinBox(QSpinBox):
    def focusInEvent(self, event):
        self.selectAll()
