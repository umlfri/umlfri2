from PyQt5.QtWidgets import QSpinBox


class SelectAllSpinBox(QSpinBox):
    def focusInEvent(self, event):
        self.selectAll()
