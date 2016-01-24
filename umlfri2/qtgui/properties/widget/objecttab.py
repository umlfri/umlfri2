from functools import partial

from PySide.QtCore import Qt
from PySide.QtGui import QTableWidgetItem

from umlfri2.qtgui.base.multiselectcombobox import MultiSelectComboBox
from ..dialog import PropertiesDialog
from .selectionchangingwidgets import QSelectionChangingCheckBox, QSelectionChangingPushButton,\
    QSelectionChangingComboBox, QSelectionChangingSpinBox, QSelectionChangingLineEdit
from umlfri2.ufl.dialog import *
from .tabletab import TableTab


class ObjectTab(TableTab):
    __tab = None
    
    def __init__(self, main_window, widget, tab):
        super().__init__()
        
        self.__main_window = main_window
        self.__widget = widget
        
        self.setRowCount(tab.widget_count)
        self.currentCellChanged.connect(self.__cell_changed)
        
        for no, widget in enumerate(tab.widgets):
            if isinstance(widget, UflDialogCheckWidget):
                qt_widget = QSelectionChangingCheckBox(self, no)
                qt_widget.stateChanged.connect(partial(self.__state_changed, widget))
            elif isinstance(widget, UflDialogChildWidget):
                qt_widget = QSelectionChangingPushButton(self, no)
                qt_widget.clicked.connect(partial(self.__show_dialog, widget))
            elif isinstance(widget, UflDialogColorWidget):
                qt_widget = QSelectionChangingPushButton(self, no) # TODO: color selection widget
            elif isinstance(widget, UflDialogComboWidget):
                qt_widget = QSelectionChangingComboBox(self, no)
                qt_widget.setEditable(True)
                for item in widget.possibilities:
                    qt_widget.addItem(item)
                qt_widget.currentIndexChanged[str].connect(partial(self.__value_changed, widget))
                qt_widget.lostFocus.connect(partial(self.__value_changed, widget))
            elif isinstance(widget, UflDialogFontWidget):
                qt_widget = QSelectionChangingPushButton(self, no) # TODO: font selection widget
            elif isinstance(widget, UflDialogIntegerWidget):
                qt_widget = QSelectionChangingSpinBox(self, no)
                qt_widget.valueChanged[int].connect(partial(self.__value_changed, widget))
            elif isinstance(widget, UflDialogMultiSelectWidget):
                qt_widget = MultiSelectComboBox()
                for checked, item in widget.possibilities:
                    qt_widget.add_check_item(checked, item)
                qt_widget.check_changed.connect(partial(self.__multi_changed, widget))
            elif isinstance(widget, UflDialogSelectWidget):
                qt_widget = QSelectionChangingComboBox(self, no)
                for item in widget.possibilities:
                    qt_widget.addItem(item)
                qt_widget.currentIndexChanged[int].connect(partial(self.__index_changed, widget))
            elif isinstance(widget, UflDialogTextWidget):
                qt_widget = QSelectionChangingLineEdit(self, no)
                qt_widget.lostFocus.connect(partial(self.__value_changed, widget))
                qt_widget.returnPressed.connect(partial(self.__value_accepted, widget, qt_widget))
            else:
                raise Exception()
            self.setCellWidget(no, 1, qt_widget)
        
        self.__tab = tab
    
    def __cell_changed(self, row, column, prev_row, prev_column):
        widget = self.cellWidget(row, 1)
        if widget is not None:
            widget.setFocus()
    
    def __show_dialog(self, widget, checked=False):
        PropertiesDialog(self.__main_window, widget.dialog, None).exec_()
        self.__widget.apply()
        
    def __state_changed(self, widget, state):
        widget.value = state == Qt.Checked
        self.__widget.apply()
    
    def __value_changed(self, widget, value):
        widget.value = value
        self.__widget.apply()
    
    def __multi_changed(self, widget, index, checked):
        if checked:
            widget.check(index)
        else:
            widget.uncheck(index)
        self.__widget.apply()
    
    def __index_changed(self, widget, index):
        widget.current_index = index
        self.__widget.apply()
    
    def __value_accepted(self, widget, qt_widget):
        widget.value = qt_widget.text()
        self.__widget.apply()
    
    def reload_data(self):
        for no, widget in enumerate(self.__tab.widgets):
            qt_widget = self.cellWidget(no, 1)
            if isinstance(widget, UflDialogCheckWidget):
                qt_widget.setChecked(widget.value)
            elif isinstance(widget, UflDialogChildWidget):
                pass
            elif isinstance(widget, UflDialogColorWidget):
                pass
            elif isinstance(widget, UflDialogComboWidget):
                qt_widget.setEditText(widget.value)
            elif isinstance(widget, UflDialogFontWidget):
                pass
            elif isinstance(widget, UflDialogIntegerWidget):
                qt_widget.setValue(widget.value)
            elif isinstance(widget, UflDialogMultiSelectWidget):
                for no, (checked, possibility) in enumerate(widget.possibilities):
                    qt_widget.set_item_checked(no, checked)
            elif isinstance(widget, UflDialogSelectWidget):
                qt_widget.setCurrentIndex(widget.current_index)
            elif isinstance(widget, UflDialogTextWidget):
                qt_widget.setText(widget.value)
            else:
                raise Exception()
    
    def reload_texts(self):
        super().reload_texts()
        
        for no, widget in enumerate(self.__tab.widgets):
            label = QTableWidgetItem(widget.label)
            label.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
            self.setItem(no, 0, label)
            
            qt_widget = self.cellWidget(no, 1)
            if isinstance(widget, UflDialogChildWidget):
                qt_widget.setText(_("Edit..."))
            elif isinstance(widget, UflDialogSelectWidget):
                for no, possibility in enumerate(widget.possibilities):
                    qt_widget.setItemText(no, possibility)
            elif isinstance(widget, UflDialogMultiSelectWidget):
                for no, (checked, possibility) in enumerate(widget.possibilities):
                    qt_widget.set_item_text(no, possibility)
    
    @property
    def label(self):
        if self.__tab.name is None:
            return _("General")
        else:
            return self.__tab.name
