from PyQt5.QtGui import QFocusEvent
from typing import Union
from umlfri2.qtgui.properties.widget.objecttab import ObjectTab
from umlfri2.qtgui.properties.widget.projecttab import ProjectTab


class QSelectionChangingCheckBox:
    def __init__(self, table: ObjectTab, row: int) -> None: ...
    def focusInEvent(self, event: QFocusEvent) -> None: ...


class QSelectionChangingComboBox:
    def __init__(self, table: ObjectTab, row: int) -> None: ...


class QSelectionChangingLineEdit:
    def __init__(
        self,
        table: Union[ObjectTab, ProjectTab],
        row: int
    ) -> None: ...
    def focusInEvent(self, event: QFocusEvent) -> None: ...
    def focusOutEvent(self, event: QFocusEvent) -> None: ...


class QSelectionChangingPushButton:
    def __init__(self, table: ObjectTab, row: int) -> None: ...
    def focusInEvent(self, event: QFocusEvent) -> None: ...
