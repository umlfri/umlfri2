from PySide.QtCore import QSize, Qt
from PySide.QtGui import QDialog, QDialogButtonBox, QVBoxLayout, QTableWidget, QHBoxLayout, QLabel, QWidget, \
    QTableWidgetItem, QFont, QStyledItemDelegate, QStyle, QPushButton, QIcon
from umlfri2.application import Application
from ..base import image_loader


class AddOnsDialog(QDialog):
    class __NoSelectionItemDelegate(QStyledItemDelegate):
        def initStyleOption(self, option, index):
            super().initStyleOption(option, index)
            
            option.state = option.state & ~QStyle.State_HasFocus
    
    def __init__(self, main_window):
        super().__init__(main_window)
        self.setWindowTitle(_("Add-ons"))
        
        self.__main_window = main_window
        
        button_box = QDialogButtonBox(QDialogButtonBox.Close)
        button_box.button(QDialogButtonBox.Close).setText(_("Close"))
        
        install_button = button_box.addButton(_("Install new..."), QDialogButtonBox.ActionRole)
        install_button.setDefault(False)
        install_button.setAutoDefault(False)
        
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
        layout.addWidget(self.__table)
        
        layout.addWidget(button_box)
        self.setLayout(layout)
        
        self.__refresh()
    
    def sizeHint(self):
        return QSize(600, 300)
    
    def __refresh(self):
        addons = list(Application().addons)
        
        self.__table.setRowCount(len(addons))
        
        for no, addon in enumerate(sorted(addons, key=lambda item: item.name)):
            if addon.icon:
                icon_item = QTableWidgetItem()
                icon_item.setIcon(image_loader.load(addon.icon))
                self.__table.setItem(no, 0, icon_item)
            
            layout = QVBoxLayout()
            layout.setSpacing(0)
            
            name_layout = QHBoxLayout()
            name_layout.setSpacing(20)
            name_layout.setAlignment(Qt.AlignLeft)
            
            name_label = QLabel(addon.name)
            name_label.setTextFormat(Qt.PlainText)
            font = name_label.font()
            font.setWeight(QFont.Bold)
            name_label.setFont(font)
            name_layout.addWidget(name_label)
            
            version_label = QLabel(str(addon.version))
            version_label.setTextFormat(Qt.PlainText)
            name_layout.addWidget(version_label)
            
            layout.addLayout(name_layout)
            
            if addon.description:
                description_label = QLabel(addon.description)
                description_label.setTextFormat(Qt.PlainText)
                description_label.setWordWrap(True)
                layout.addWidget(description_label)
            
            addon_button_box = QHBoxLayout()
            addon_button_box.setAlignment(Qt.AlignRight)
            addon_button_box.setContentsMargins(0, 5, 0, 0)
            
            start_button = QPushButton(QIcon.fromTheme("media-playback-start"), _("Start"))
            start_button.setEnabled(not addon.is_started)
            addon_button_box.addWidget(start_button)
            
            stop_button = QPushButton(QIcon.fromTheme("media-playback-stop"), _("Stop"))
            stop_button.setEnabled(addon.is_started)
            addon_button_box.addWidget(stop_button)
            
            if addon.has_config:
                preferences_button = QPushButton(QIcon.fromTheme("preferences-other"), _("Preferences"))
                addon_button_box.addWidget(preferences_button)
            
            uninstall_button = QPushButton(QIcon.fromTheme("edit-delete"), _("Uninstall"))
            addon_button_box.addWidget(uninstall_button)
            
            addon_button_box_widget = QWidget()
            addon_button_box_widget.setLayout(addon_button_box)
            addon_button_box_widget.setVisible(False)
            
            layout.addWidget(addon_button_box_widget)
            
            widget = QWidget()
            widget.setLayout(layout)
            self.__table.setCellWidget(no, 1, widget)
        
        self.__table.resizeColumnsToContents()
        self.__table.resizeRowsToContents()
    
    def __selection_changed(self):
        selection = set(item.row() for item in self.__table.selectedIndexes())
        
        for i in range(self.__table.rowCount()):
            cell = self.__table.cellWidget(i, 1)
            cellLayout = cell.layout()
            button_box = cellLayout.itemAt(cellLayout.count() - 1)
            if i in selection:
                button_box.widget().show()
            else:
                button_box.widget().hide()
        
        self.__table.resizeRowsToContents()
