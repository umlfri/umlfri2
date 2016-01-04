from functools import partial

from PySide.QtCore import Qt
from PySide.QtGui import QTableWidgetItem

from ..dialog import PropertiesDialog
from .selectionchangingwidgets import QSelectionChangingCheckBox, QSelectionChangingPushButton,\
    QSelectionChangingComboBox, QSelectionChangingSpinBox, QSelectionChangingLineEdit
from umlfri2.ufl.dialog import *
from .tabletab import TableTab


class ObjectTab(TableTab):
    __tab = None
    
    def __init__(self, main_window, tab, dialog):
        super().__init__()
        
        self.__main_window = main_window
        
        self.setRowCount(tab.widget_count)
        self.itemChanged.connect(self.__item_changed)
        self.currentCellChanged.connect(self.__cell_changed)
        
        for no, widget in enumerate(tab.widgets):
            if isinstance(widget, UflDialogCheckWidget):
                qt_widget = QSelectionChangingCheckBox(self, no)
                qt_widget.setChecked(widget.value)
            elif isinstance(widget, UflDialogChildWidget):
                qt_widget = QSelectionChangingPushButton(self, no)
                qt_widget.clicked.connect(partial(self.__show_dialog, widget.dialog))
            elif isinstance(widget, UflDialogColorWidget):
                qt_widget = QSelectionChangingPushButton(self, no) # TODO: color selection widget
            elif isinstance(widget, UflDialogComboWidget):
                qt_widget = QSelectionChangingComboBox(self, no)
                qt_widget.setEditable(True)
                for item in widget.possibilities:
                    qt_widget.addItem(item)
                qt_widget.setEditText(widget.value)
            elif isinstance(widget, UflDialogFontWidget):
                qt_widget = QSelectionChangingPushButton(self, no) # TODO: font selection widget
            elif isinstance(widget, UflDialogIntegerWidget):
                qt_widget = QSelectionChangingSpinBox(self, no)
                qt_widget.setValue(widget.value)
            elif isinstance(widget, UflDialogSelectWidget):
                qt_widget = QSelectionChangingComboBox(self, no)
                for item in widget.possibilities:
                    qt_widget.addItem(item)
                qt_widget.setCurrentIndex(widget.current_index)
            elif isinstance(widget, UflDialogTextWidget):
                qt_widget = QSelectionChangingLineEdit(self, no)
                qt_widget.setText(widget.value)
            else:
                raise Exception()
            self.setCellWidget(no, 1, qt_widget)
        
        self.__tab = tab
        self.__dialog = dialog
    
    def __item_changed(self, item):
        pass
    
    def __cell_changed(self, row, column, prev_row, prev_column):
        widget = self.cellWidget(row, 1)
        if widget is not None:
            widget.setFocus()
    
    def __show_dialog(self, dialog, checked=False):
        PropertiesDialog(self.__main_window, dialog, None).exec_()
    
    def reload_texts(self):
        super().reload_texts()
        
        for no, widget in enumerate(self.__tab.widgets):
            label = QTableWidgetItem(widget.label)
            label.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.setItem(no, 0, label)
            
            if isinstance(widget, UflDialogChildWidget):
                self.cellWidget(no, 1).setText(_("Edit..."))
    
    @property
    def label(self):
        if self.__tab.name is None:
            return _("General")
        else:
            return self.__tab.name
