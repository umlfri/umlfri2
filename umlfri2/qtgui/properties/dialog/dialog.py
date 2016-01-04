from PySide.QtCore import QSize, Qt
from PySide.QtGui import QDialog, QDialogButtonBox, QVBoxLayout, QTabWidget

from umlfri2.application import Application
from umlfri2.application.commands.model import ApplyPatchCommand
from .listtab import ListPropertyTab
from .objecttab import ObjectPropertyTab
from umlfri2.ufl.dialog import UflDialogListTab, UflDialogObjectTab, UflDialogValueTab


class PropertiesDialog(QDialog):
    def __init__(self, main_window, dialog, object): 
        super().__init__(main_window)
        self.__main_window = main_window
        self.setWindowTitle(_("Properties"))
        self.__dialog = dialog
        self.__object = object
        
        if object:
            button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel | QDialogButtonBox.Apply)
            button_box.button(QDialogButtonBox.Ok).setText(_("Ok"))
            button_box.button(QDialogButtonBox.Cancel).setText(_("Cancel"))
            apply_button = button_box.button(QDialogButtonBox.Apply)
            apply_button.setText(_("Apply"))
            apply_button.clicked.connect(self.__apply_clicked)
        else:
            button_box = QDialogButtonBox(QDialogButtonBox.Ok)
            button_box.button(QDialogButtonBox.Ok).setText(_("Ok"))
        
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout = QVBoxLayout()
        
        tab = dialog.get_lonely_tab()
        if isinstance(tab, UflDialogListTab):
            layout.addWidget(ListPropertyTab(self, tab))
        elif isinstance(tab, (UflDialogObjectTab, UflDialogValueTab)):
            layout.addWidget(ObjectPropertyTab(self, tab))
        else:
            tabs = QTabWidget()
            tabs.setFocusPolicy(Qt.NoFocus)
            
            for tab in dialog.tabs:
                if isinstance(tab, UflDialogListTab):
                    tabs.addTab(ListPropertyTab(self, tab), tab.name or _("General"))
                elif isinstance(tab, (UflDialogObjectTab, UflDialogValueTab)):
                    tabs.addTab(ObjectPropertyTab(self, tab), tab.name or _("General"))
            layout.addWidget(tabs)
        
        layout.addWidget(button_box)
        self.setLayout(layout)
    
    def sizeHint(self):
        orig = super().sizeHint()
        return QSize(500, orig.height())
    
    def __apply_clicked(self, checked=False):
        self.__dialog.finish()
        command = ApplyPatchCommand(self.__object, self.__dialog.make_patch())
        Application().commands.execute(command)
        self.__dialog.reset()
    
    @staticmethod
    def open_for(main_window, object):
        dialog = object.create_ufl_dialog()
        dialog.translate(object.type.metamodel.addon.get_translation(Application().language))
        qt_dialog = PropertiesDialog(main_window, dialog, object)
        qt_dialog.setModal(True)
        if qt_dialog.exec_() == PropertiesDialog.Accepted:
            dialog.finish()
            command = ApplyPatchCommand(object, dialog.make_patch())
            Application().commands.execute(command)
