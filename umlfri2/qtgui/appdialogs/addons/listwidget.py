from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QFont, QPalette
from PyQt5.QtWidgets import QVBoxLayout, QTableWidget, QHBoxLayout, QLabel, QWidget,  QStyledItemDelegate, QStyle

from umlfri2.application.addon.online import OnlineAddOn
from umlfri2.qtgui.base import image_loader


class AddOnListWidget(QTableWidget):
    class __NoSelectionItemDelegate(QStyledItemDelegate):
        def initStyleOption(self, option, index):
            super().initStyleOption(option, index)
            
            option.state = option.state & ~QStyle.State_HasFocus
    
    def __init__(self):
        super().__init__()
        
        self.setTabKeyNavigation(False)
        self.setItemDelegate(self.__NoSelectionItemDelegate())
        self.verticalHeader().hide()
        self.horizontalHeader().hide()
        self.setColumnCount(2)
        self.setSelectionBehavior(QTableWidget.SelectRows)
        self.setSelectionMode(QTableWidget.SingleSelection)
        self.horizontalHeader().setStretchLastSection(True)
        self.setAlternatingRowColors(True)
        self.setShowGrid(False)
        self.setIconSize(QSize(32, 32))
        self.itemSelectionChanged.connect(self.__selection_changed)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.__context_menu_requested)
        
        self.refresh()
    
    @property
    def _addons(self):
        raise NotImplementedError
    
    def _addon_button_factory(self):
        raise NotImplementedError
    
    def _addon_content_menu(self, addon):
        raise NotImplementedError
    
    def refresh(self):
        addons = sorted(self._addons, key=lambda item: item.name)
        self.__addons = list(addons)
        
        button_factory = self._addon_button_factory()
        
        self.setRowCount(len(self.__addons))
        
        for no, addon in enumerate(self.__addons):
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
                
                self.setCellWidget(no, 0, icon_widget)
            
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
            
            if isinstance(addon, OnlineAddOn):
                version = addon.latest_version.version
            else:
                version = addon.version
            
            version_label = QLabel(str(version))
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
            
            if button_factory is not None:
                button_factory.add_buttons(addon, addon_button_box)
            
            if addon_button_box.count() > 0:
                addon_button_box_widget = QWidget()
                addon_button_box_widget.setLayout(addon_button_box)
                addon_button_box_widget.setVisible(False)
                addon_button_box_widget.setObjectName("button_box")
                
                layout.addWidget(addon_button_box_widget)
            
            widget = QWidget()
            widget.setLayout(layout)
            self.setCellWidget(no, 1, widget)

            self.__refresh_selection_colors(widget, False)
        
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
    
    def __selection_changed(self):
        selection = set(item.row() for item in self.selectedIndexes())
        
        for i in range(self.rowCount()):
            cell = self.cellWidget(i, 1)
            button_box = cell.findChild(QWidget, "button_box")
            
            if button_box is not None: # no button box present
                if i in selection:
                    button_box.show()
                else:
                    button_box.hide()
            
            self.__refresh_selection_colors(cell, i in selection)
        
        self.resizeRowsToContents()
    
    def __refresh_selection_colors(self, cell_widget, selected):
        if selected:
            color = self.palette().color(QPalette.Active, QPalette.HighlightedText)
        else:
            color = self.palette().color(QPalette.Active, QPalette.Text)
            
        for lbl in cell_widget.findChildren(QLabel):
            lbl.setStyleSheet("QLabel {{ color : {0}; }}".format(color.name()))
    
    def __context_menu_requested(self, point):
        index = self.indexAt(point)
        
        addon = self.__addons[index.row()]
        
        menu = self._addon_content_menu(addon)
        
        if menu is not None:
            menu.exec_(self.viewport().mapToGlobal(point))
