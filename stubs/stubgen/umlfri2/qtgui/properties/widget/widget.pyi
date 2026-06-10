from .emptytab import EmptyTab as EmptyTab
from .nullabletexttab import NullableTextTab as NullableTextTab
from .objecttab import ObjectTab as ObjectTab
from .projecttab import ProjectTab as ProjectTab
from .texttab import TextTab as TextTab
from PyQt5.QtWidgets import QTabWidget
from umlfri2.application import Application as Application
from umlfri2.application.commands.model import ApplyPatchCommand as ApplyPatchCommand
from umlfri2.application.events.application import ItemSelectedEvent as ItemSelectedEvent, LanguageChangedEvent as LanguageChangedEvent
from umlfri2.application.events.diagram import SelectionChangedEvent as SelectionChangedEvent
from umlfri2.application.events.model import ConnectionDeletedEvent as ConnectionDeletedEvent, DiagramDeletedEvent as DiagramDeletedEvent, ElementDeletedEvent as ElementDeletedEvent, ObjectDataChangedEvent as ObjectDataChangedEvent, ProjectChangedEvent as ProjectChangedEvent
from umlfri2.application.events.solution import CloseSolutionEvent as CloseSolutionEvent
from umlfri2.application.events.tabs import ChangedCurrentTabEvent as ChangedCurrentTabEvent
from umlfri2.model import Project as Project
from umlfri2.ufl.dialog import UflDialogNullableValueTab as UflDialogNullableValueTab, UflDialogObjectTab as UflDialogObjectTab, UflDialogOptions as UflDialogOptions, UflDialogValueTab as UflDialogValueTab

class PropertiesWidget(QTabWidget):
    def __init__(self, main_window) -> None: ...
    def apply(self) -> None: ...
