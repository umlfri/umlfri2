from collections import namedtuple
from functools import partial

from PyQt5.QtCore import QSize, Qt, QUrl, QTimer
from PyQt5.QtGui import QFont, QIcon, QDesktopServices, QPalette
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QTableWidget, QHBoxLayout, QLabel, QWidget, \
    QTableWidgetItem, QStyledItemDelegate, QStyle, QPushButton, QMenu, QFileDialog
from umlfri2.application import Application
from umlfri2.application.addon import AddOnState
from umlfri2.application.events.addon import AddonStateChangedEvent
from umlfri2.datalayer import Storage
from umlfri2.qtgui.base import image_loader
from .info import AddOnInfo


class AddOnsDialog(QDialog):
    class __NoSelectionItemDelegate(QStyledItemDelegate):
        def initStyleOption(self, option, index):
            super().initStyleOption(option, index)
            
            option.state = option.state & ~QStyle.State_HasFocus
    
    __AddonButtons = namedtuple('AddonButtons', ['start', 'stop'])
    
    def __init__(self, main_window):
        super().__init__(main_window)
        self.setWindowTitle(_("Add-ons"))
        
        self.__main_window = main_window
        
        button_box = QDialogButtonBox(QDialogButtonBox.Close)
        button_box.button(QDialogButtonBox.Close).setText(_("Close"))
        
        install_button = button_box.addButton(_("Install new..."), QDialogButtonBox.ActionRole)
        install_button.setDefault(False)
        install_button.setAutoDefault(False)
        install_button.clicked.connect(self.__install_addon)
        
        button_box.rejected.connect(self.reject)
        
        layout = QVBoxLayout()
        
        self.__table = QTableWidget()
        self.__table.setItemDelegate(self.__NoSelectionItemDelegate())
        self.__table.verticalHeader().hide()
        self.__table.horizontalHeader().hide()
        self.__table.setColumnCount(2)
        self.__table.setSelectionBehavior(QTableWidget.SelectRows)
        self.__table.setSelectionMode(QTableWidget.SingleSelection)
        self.__table.horizontalHeader().setStretchLastSection(True)
        self.__table.setAlternatingRowColors(True)
        self.__table.setShowGrid(False)
        self.__table.setIconSize(QSize(32, 32))
        self.__table.itemSelectionChanged.connect(self.__selection_changed)
        self.__table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.__table.customContextMenuRequested.connect(self.__context_menu_requested)
        layout.addWidget(self.__table)
        
        layout.addWidget(button_box)
        self.setLayout(layout)

        self.__timer = QTimer(self)
        self.__timer.timeout.connect(self.__timer_event)
        
        Application().event_dispatcher.subscribe(AddonStateChangedEvent, self.__addon_state_changed)
        
        self.__refresh()
    
    def sizeHint(self):
        return QSize(600, 300)
    
    def closeEvent(self, event):
        if self.isEnabled():
            super().closeEvent(event)
        else:
            event.ignore()
    
    def __refresh(self):
        addons = sorted(Application().addons, key=lambda item: item.name)
        self.__addons = addons
        self.__addon_buttons = {}
        
        self.__table.setRowCount(len(addons))
        
        for no, addon in enumerate(addons):
            if addon.icon:
                icon_widget = QWidget()
                icon_layout = QVBoxLayout()
                icon_layout.setSpacing(0)
                icon_widget.setLayout(icon_layout)
                icon_label = QLabel()
                icon_label.setAutoFillBackground(False)
                icon_label.setPixmap(image_loader.load(addon.icon))
                icon_label.setAlignment(Qt.AlignTop)
                icon_layout.addWidget(icon_label)
                
                lp, tp, rp, bp = icon_layout.getContentsMargins()
                icon_layout.setContentsMargins(lp, tp, 0, bp)
                
                self.__table.setCellWidget(no, 0, icon_widget)
            
            layout = QVBoxLayout()
            layout.setSpacing(0)
            layout.setAlignment(Qt.AlignTop)
            
            name_layout = QHBoxLayout()
            name_layout.setSpacing(20)
            name_layout.setAlignment(Qt.AlignLeft)
            
            name_label = QLabel(addon.name)
            name_label.setAutoFillBackground(False)
            name_label.setTextFormat(Qt.PlainText)
            font = name_label.font()
            font.setWeight(QFont.Bold)
            name_label.setFont(font)
            name_layout.addWidget(name_label)
            
            version_label = QLabel(str(addon.version))
            version_label.setAutoFillBackground(False)
            version_label.setTextFormat(Qt.PlainText)
            name_layout.addWidget(version_label)
            
            layout.addLayout(name_layout)
            
            if addon.description:
                description_label = QLabel(addon.description)
                description_label.setAutoFillBackground(False)
                description_label.setTextFormat(Qt.PlainText)
                description_label.setWordWrap(True)
                layout.addWidget(description_label)
            
            addon_button_box = QHBoxLayout()
            addon_button_box.setAlignment(Qt.AlignRight)
            
            if addon.state != AddOnState.none:
                start_button = QPushButton(QIcon.fromTheme("media-playback-start"), _("Start"))
                start_button.setFocusPolicy(Qt.NoFocus)
                start_button.setEnabled(addon.state in (AddOnState.stopped, AddOnState.error))
                start_button.clicked.connect(partial(self.__start_addon, addon))
                addon_button_box.addWidget(start_button)
                
                stop_button = QPushButton(QIcon.fromTheme("media-playback-stop"), _("Stop"))
                stop_button.setFocusPolicy(Qt.NoFocus)
                stop_button.setEnabled(addon.state == AddOnState.started)
                stop_button.clicked.connect(partial(self.__stop_addon, addon))
                addon_button_box.addWidget(stop_button)
                
                self.__addon_buttons[addon.identifier] = self.__AddonButtons(start_button, stop_button)
            
            if addon_button_box.count() > 0:
                addon_button_box_widget = QWidget()
                addon_button_box_widget.setLayout(addon_button_box)
                addon_button_box_widget.setVisible(False)
                addon_button_box_widget.setObjectName("button_box")
                
                layout.addWidget(addon_button_box_widget)
            
            widget = QWidget()
            widget.setLayout(layout)
            self.__table.setCellWidget(no, 1, widget)

            self.__refresh_selection_colors(widget, False)
        
        self.__table.resizeColumnsToContents()
        self.__table.resizeRowsToContents()
    
    def __addon_state_changed(self, event):
        if event.addon.identifier in self.__addon_buttons:
            buttons = self.__addon_buttons[event.addon.identifier]
            buttons.start.setEnabled(event.addon.state in (AddOnState.stopped, AddOnState.error))
            buttons.stop.setEnabled(event.addon.state == AddOnState.started)
    
    def __selection_changed(self):
        selection = set(item.row() for item in self.__table.selectedIndexes())
        
        for i in range(self.__table.rowCount()):
            cell = self.__table.cellWidget(i, 1)
            button_box = cell.findChild(QWidget, "button_box")
            
            if button_box is not None: # no button box present
                if i in selection:
                    button_box.show()
                else:
                    button_box.hide()
            
            self.__refresh_selection_colors(cell, i in selection)
        
        self.__table.resizeRowsToContents()
    
    def __refresh_selection_colors(self, cell_widget, selected):
        if selected:
            color = self.__table.palette().color(QPalette.Active, QPalette.HighlightedText)
        else:
            color = self.__table.palette().color(QPalette.Active, QPalette.Text)
            
        for lbl in cell_widget.findChildren(QLabel):
            lbl.setStyleSheet("QLabel {{ color : {0}; }}".format(color.name()))
    
    def __context_menu_requested(self, point):
        index = self.__table.indexAt(point)
        
        addon = self.__addons[index.row()]
        
        menu = QMenu(self.__table)
        
        if addon.state != AddOnState.none:
            start = menu.addAction(QIcon.fromTheme("media-playback-start"), _("Start"))
            stop = menu.addAction(QIcon.fromTheme("media-playback-stop"), _("Stop"))

            start.triggered.connect(partial(self.__start_addon, addon))
            stop.triggered.connect(partial(self.__stop_addon, addon))
            
            if addon.state == AddOnState.started:
                start.setEnabled(False)

            if addon.state in (AddOnState.stopped, AddOnState.error):
                stop.setEnabled(False)
            
            menu.addSeparator()
        
        if addon.homepage:
            homepage = menu.addAction(QIcon.fromTheme("application-internet"), _("Homepage"))
            homepage.triggered.connect(partial(self.__show_homepage, addon))
        about = menu.addAction(QIcon.fromTheme("help-about"), _("About..."))
        about.triggered.connect(partial(self.__show_info, addon))
        
        menu.addSeparator()

        if not addon.is_system_addon:
            menu.addAction(QIcon.fromTheme("edit-delete"), _("Uninstall"))
        
        menu.exec_(self.__table.viewport().mapToGlobal(point))
    
    def __install_addon(self):
        file_name, filter = QFileDialog.getOpenFileName(
                self,
                caption=_("Install AddOn From File"),
                filter=_("UML .FRI 2 addons") + "(*.fria2)"
        )
        if file_name:
            Application().addons.install_addon(Storage.read_storage(file_name))
    
    def __show_homepage(self, addon, checked=False):
        QDesktopServices.openUrl(QUrl(addon.homepage))
    
    def __show_info(self, addon, checked=False):
        dialog = AddOnInfo(self, addon)
        dialog.exec_()
    
    def __start_addon(self, addon, checked=False):
        self.__run_process(addon.start())

    def __stop_addon(self, addon, checked=False):
        self.__run_process(addon.stop())
    
    def __run_process(self, starter_stopper):
        self.__starter_stopper = starter_stopper
        self.__timer.start(100)
        self.__timer_event()
        self.setEnabled(False)
        
    def __timer_event(self):
        if self.__starter_stopper.finished:
            self.__timer.stop()
            self.setEnabled(True)
        else:
            self.__starter_stopper.do()
