from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QTabWidget, QMessageBox

from umlfri2.application import Application
from umlfri2.application.commands.model import ApplyPatchCommand
from umlfri2.application.commands.solution import ApplyMetamodelConfigPatchCommand
from umlfri2.qtgui.base.validatingtabwidget import ValidatingTabWidget
from .listtab import ListPropertyTab
from .objecttab import ObjectPropertyTab
from umlfri2.ufl.dialog import UflDialogListTab, UflDialogObjectTab, UflDialogValueTab, UflDialogNullableValueTab


class PropertiesDialog(QDialog):
    def __init__(self, main_window, dialog, mk_apply_patch_command):
        super().__init__(main_window)
        self.__main_window = main_window
        self.setWindowTitle(_("Properties"))
        self.__dialog = dialog
        self.__mk_apply_patch_command = mk_apply_patch_command
        
        if mk_apply_patch_command:
            button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel | QDialogButtonBox.Apply)
            button_box.button(QDialogButtonBox.Ok).setText(_("Ok"))
            button_box.button(QDialogButtonBox.Cancel).setText(_("Cancel"))
            apply_button = button_box.button(QDialogButtonBox.Apply)
            apply_button.setText(_("Apply"))
            apply_button.clicked.connect(self.__apply_clicked)
        else:
            button_box = QDialogButtonBox(QDialogButtonBox.Ok)
            button_box.button(QDialogButtonBox.Ok).setText(_("Ok"))
        
        button_box.accepted.connect(self.__accept_clicked)
        button_box.rejected.connect(self.reject)
        layout = QVBoxLayout()
        
        self.__tabs = []
        tab = dialog.get_lonely_tab()
        if isinstance(tab, UflDialogListTab):
            qt_tab = ListPropertyTab(self, tab, lonely=True)
            layout.addWidget(qt_tab)
            self.__tabs.append(qt_tab)
        elif isinstance(tab, (UflDialogObjectTab, UflDialogValueTab)):
            qt_tab = ObjectPropertyTab(self, tab, lonely=True)
            layout.addWidget(qt_tab)
            self.__tabs.append(qt_tab)
        else:
            self.__tab_widget = ValidatingTabWidget()
            self.__tab_widget.setFocusPolicy(Qt.NoFocus)
            self.__tab_widget.currentChanged.connect(self.__tab_changed)
            self.__tab_widget.tabBar().validate_tab_change.connect(self.__validate_tab)
            
            for tab in dialog.tabs:
                if isinstance(tab, UflDialogListTab):
                    qt_tab = ListPropertyTab(self, tab)
                elif isinstance(tab, (UflDialogObjectTab, UflDialogValueTab)):
                    qt_tab = ObjectPropertyTab(self, tab)
                self.__tab_widget.addTab(qt_tab, tab.name or _("General"))
                self.__tabs.append(qt_tab)
            layout.addWidget(self.__tab_widget)
        
        layout.addWidget(button_box)
        self.setLayout(layout)
    
    def closeEvent(self, event):
        if self.__dialog.has_changes:
            message_box = QMessageBox(self)
            message_box.setWindowModality(Qt.WindowModal)
            message_box.setIcon(QMessageBox.Question)
            message_box.setWindowTitle(_("Properties has been changed"))
            message_box.setText(_("Properties in this dialog was changed, but not applied."))
            message_box.setInformativeText(_("Do you want to apply the changes?"))
            message_box.setStandardButtons(QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel)
            message_box.setDefaultButton(QMessageBox.Save)
            message_box.button(QMessageBox.Save).setText(_("Apply"))
            message_box.button(QMessageBox.Discard).setText(_("Close without applying"))
            message_box.button(QMessageBox.Cancel).setText(_("Cancel"))
            resp = message_box.exec()
            
            if resp == QMessageBox.Save:
                self.__accept_clicked()
            elif resp == QMessageBox.Cancel:
                event.ignore()
    
    def sizeHint(self):
        orig = super().sizeHint()
        return QSize(500, orig.height())
    
    def __apply_clicked(self, checked=False):
        if self.__dialog.should_save_tab:
            if not self.__tabs[self.__dialog.current_tab.tab_index].handle_needed_save():
                return
        
        self.__dialog.finish()
        command = self.__mk_apply_patch_command(self.__dialog.make_patch())
        Application().commands.execute(command)
        self.__dialog.reset()
        
        for tab in self.__tabs:
            tab.refresh()
    
    def __accept_clicked(self):
        if self.__dialog.should_save_tab:
            if not self.__tabs[self.__dialog.current_tab.tab_index].handle_needed_save():
                return

        self.__dialog.finish()
        
        if self.__mk_apply_patch_command is not None:
            command = self.__mk_apply_patch_command(self.__dialog.make_patch())
            Application().commands.execute(command)
        
        self.accept()
    
    def __tab_changed(self, tab_index):
        self.__dialog.switch_tab(tab_index)

        for tab in self.__tabs:
            tab.refresh()
    
    def __validate_tab(self, event):
        if self.__dialog.should_save_tab:
            if not self.__tabs[self.__dialog.current_tab.tab_index].handle_needed_save():
                event.invalidate()
                return
    
    @staticmethod
    def open_for(main_window, object):
        dialog = object.create_ufl_dialog()
        dialog.translate(object.type.metamodel.get_translation(Application().language.current_language))
        qt_dialog = PropertiesDialog(main_window, dialog, lambda patch: ApplyPatchCommand(object, patch))
        qt_dialog.setModal(True)
        qt_dialog.exec_()
    
    @staticmethod
    def open_config(main_window, project):
        dialog = project.create_config_dialog()
        dialog.translate(project.metamodel.get_translation(Application().language.current_language))
        solution = Application().solution
        qt_dialog = PropertiesDialog(main_window, dialog, lambda patch: ApplyMetamodelConfigPatchCommand(solution, project, patch))
        qt_dialog.setModal(True)
        qt_dialog.exec_()
