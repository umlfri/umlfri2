from umlfri2.ufl.dialog import *
from ..dialog import PropertiesDialog as PropertiesDialog
from .selectionchangingwidgets import QSelectionChangingCheckBox as QSelectionChangingCheckBox, QSelectionChangingComboBox as QSelectionChangingComboBox, QSelectionChangingDoubleSpinBox as QSelectionChangingDoubleSpinBox, QSelectionChangingLineEdit as QSelectionChangingLineEdit, QSelectionChangingPushButton as QSelectionChangingPushButton, QSelectionChangingSpinBox as QSelectionChangingSpinBox
from .tabletab import TableTab as TableTab
from umlfri2.qtgui.base.colorwidget import ColorSelectionWidget as ColorSelectionWidget
from umlfri2.qtgui.base.fontwidget import FontSelectionWidget as FontSelectionWidget
from umlfri2.qtgui.base.multiselectcombobox import MultiSelectComboBox as MultiSelectComboBox

class ObjectTab(TableTab):
    def __init__(self, main_window, widget, tab) -> None: ...
    def reload_data(self) -> None: ...
    def reload_texts(self) -> None: ...
    @property
    def label(self): ...
