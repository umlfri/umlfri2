from PySide.QtGui import QCheckBox, QPushButton, QComboBox, QSpinBox, QLineEdit


class QSelectionChangingCheckBox(QCheckBox):
    def __init__(self, table, row):
        super().__init__()
        self.__table = table
        self.__row = row
    
    def focusInEvent(self, event):
        super().focusInEvent(event)
        
        self.__table.setCurrentCell(self.__row, 1)


class QSelectionChangingPushButton(QPushButton):
    def __init__(self, table, row):
        super().__init__()
        self.__table = table
        self.__row = row
    
    def focusInEvent(self, event):
        super().focusInEvent(event)
        
        self.__table.setCurrentCell(self.__row, 1)


class QSelectionChangingComboBox(QComboBox):
    def __init__(self, table, row):
        super().__init__()
        self.__table = table
        self.__row = row
    
    def focusInEvent(self, event):
        super().focusInEvent(event)
        
        self.__table.setCurrentCell(self.__row, 1)


class QSelectionChangingSpinBox(QSpinBox):
    def __init__(self, table, row):
        super().__init__()
        self.__table = table
        self.__row = row
    
    def focusInEvent(self, event):
        super().focusInEvent(event)
        
        self.__table.setCurrentCell(self.__row, 1)


class QSelectionChangingLineEdit(QLineEdit):
    def __init__(self, table, row):
        super().__init__()
        self.__table = table
        self.__row = row
    
    def focusInEvent(self, event):
        super().focusInEvent(event)
        
        self.__table.setCurrentCell(self.__row, 1)
