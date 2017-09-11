from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLineEdit


class SelectAllLineEdit(QLineEdit):
    def focusInEvent(self, event):
        super().focusInEvent(event)
        
        if event.reason() in (Qt.TabFocusReason, Qt.BacktabFocusReason, Qt.ActiveWindowFocusReason):
            self.selectAll()
