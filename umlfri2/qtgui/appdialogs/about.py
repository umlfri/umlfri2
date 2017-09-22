import os.path

from PyQt5.QtCore import QSize, pyqtSignal, Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QVBoxLayout, QLabel, QSpacerItem, QDialogButtonBox, QTabWidget, \
    QTextEdit, QGridLayout, QFormLayout, QScrollArea, QWidget, QPushButton

from umlfri2.application import Application
from umlfri2.application.events.application import UpdateCheckStartedEvent, UpdateCheckFinishedEvent
from umlfri2.constants.paths import GRAPHICS, LICENSE_FILE
from umlfri2.qtgui.exceptionhook import ExceptionDialog


class AboutDialog(QDialog):
    __update_finished_evt = pyqtSignal()
    
    def __init__(self, main_window):
        super().__init__(main_window)
        
        self.setWindowTitle(_("About UML .FRI"))
        
        main_layout = QVBoxLayout()
        
        desc_layout = QHBoxLayout()
        
        logo_pixmap = QPixmap()
        logo_pixmap.load(os.path.join(GRAPHICS, "logo", "logo_full.png"))
        
        logo = QLabel()
        logo.setPixmap(logo_pixmap)
        
        desc_layout.addWidget(logo, 0, Qt.AlignTop)
        
        desc_text_layout = QVBoxLayout()
        
        desc_text_layout.addWidget(QLabel("<h1>{0}</h1>".format(Application().about.name)))
        desc_text_layout.addWidget(QLabel("{0} {1}".format(_("Version"), Application().about.version)))
        desc_text_layout.addItem(QSpacerItem(0, 20))
        desc_label = QLabel(Application().about.description)
        desc_label.setWordWrap(True)
        desc_text_layout.addWidget(desc_label)
        desc_text_layout.addStretch(1)
        for author, year in Application().about.author:
            desc_text_layout.addWidget(QLabel("<small>{0}</small>".format(self.__about_line(author, year))))
        
        for url in Application().about.urls:
            desc_text_layout.addWidget(self.__create_link(url))
        
        desc_layout.addLayout(desc_text_layout, 1)
        
        main_layout.addLayout(desc_layout)
        
        tabs = QTabWidget()
        tabs.setUsesScrollButtons(False)
        main_layout.addWidget(tabs, 1)

        self.__updates_tab = None
        
        tabs.addTab(self.__create_used_libraries_tab(), _("Used libraries"))
        
        if os.path.exists(LICENSE_FILE):
            tabs.addTab(self.__create_license_tab(), _("License"))
        
        tabs.addTab(self.__create_version_1_0_tab(), _("Version 1.0 contributions"))

        tabs.addTab(self.__create_updates_tab(), _("Updates"))
        
        if Application().about.is_debug_version:
            debug_layout = QHBoxLayout()
            debug_icon = QLabel()
            debug_icon.setPixmap(QIcon.fromTheme("dialog-warning").pixmap(QSize(16, 16)))
            debug_layout.addWidget(debug_icon)
            debug_text = QLabel(_("You are running UML .FRI in the debug mode"))
            debug_layout.addWidget(debug_text, 1)
            main_layout.addLayout(debug_layout)
        
        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.button(QDialogButtonBox.Ok).setText(_("Ok"))
        button_box.accepted.connect(self.accept)
        
        main_layout.addWidget(button_box)
        
        self.setLayout(main_layout)
        
        self.__update_finished_evt.connect(self.__create_updates_tab)
        
        Application().event_dispatcher.subscribe(UpdateCheckStartedEvent, self.__update_started)
        Application().event_dispatcher.subscribe(UpdateCheckFinishedEvent, self.__update_finished)
    
    def __create_used_libraries_tab(self):
        versions_layout = QFormLayout()
        for depencency, version in Application().about.dependency_versions:
            versions_layout.addRow(_("{0} version").format(depencency), QLabel(version))
        versions_widget = QWidget()
        versions_widget.setLayout(versions_layout)
        return versions_widget
    
    def __create_license_tab(self):
        license_text = QTextEdit()
        with open(LICENSE_FILE, 'rt') as license_file:
            license_text.setPlainText(license_file.read())
        license_text.setReadOnly(True)
        license_text.setLineWrapMode(QTextEdit.NoWrap)
        return license_text
    
    def __create_version_1_0_tab(self):
        version_1_layout = QVBoxLayout()
        for author, year in Application().about.version_1_contributions:
            version_1_layout.addWidget(QLabel(self.__about_line(author, year)))
        version_1_widget = QWidget()
        version_1_widget.setLayout(version_1_layout)
        version_1_scroll = QScrollArea()
        version_1_scroll.setWidget(version_1_widget)
        return version_1_scroll
    
    def __create_updates_tab(self):
        if self.__updates_tab is None:
            self.__updates_tab = QWidget()
        else:
            self.__updates_tab.children()[0].deleteLater()
        
        updates_layout = QGridLayout()
        updates_widget = QWidget(self.__updates_tab)
        updates_widget.setLayout(updates_layout)
        self.__check_updates = QPushButton(_("Check for updates"))
        self.__check_updates.clicked.connect(lambda checked=False: Application().about.updates.recheck_update())
        updates_layout.addWidget(self.__check_updates, 0, 0, 1, 3, Qt.AlignLeft)
        updates_layout.addWidget(QLabel(_("Latest version available:")), 1, 0)
        if Application().about.updates.latest_version is None:
            updates_layout.addWidget(QLabel("-"), 1, 1)
        else:
            updates_layout.addWidget(QLabel(str(Application().about.updates.latest_version)), 1, 1)
        if Application().about.updates.has_newer_version:
            updates_layout.addWidget(self.__create_download_link(Application().about.updates.version_update_url), 1, 2)
        if Application().about.updates.latest_prerelease is not None:
            updates_layout.addWidget(QLabel(_("Latest unstable version available:")), 2, 0)
            updates_layout.addWidget(QLabel(str(Application().about.updates.latest_prerelease)), 2, 1)

            if Application().about.updates.has_newer_prerelease:
                updates_layout.addWidget(self.__create_download_link(Application().about.updates.prerelease_update_url), 2, 2)
        if Application().about.updates.has_error:
            updates_layout.addWidget(QLabel("<b>{0}</b>".format(_("Error while checking update:"))), 3, 0)
            more_info = QPushButton(_("More info"))
            more_info.clicked.connect(self.__show_update_error)
            updates_layout.addWidget(more_info, 3, 1)
            
        updates_widget.setVisible(True)
        return self.__updates_tab
    
    def __show_update_error(self, checked=False):
        ExceptionDialog(Application().about.updates.error).exec()
    
    def __create_link(self, url):
        ret = QLabel("<a href=\"{0}\">{1}</a>".format(url, url))
        ret.setOpenExternalLinks(True)
        return ret
    
    def __create_download_link(self, url):
        ret = QLabel("<a href=\"{0}\">{1}</a>".format(url, _("download update")))
        ret.setToolTip(url)
        ret.setOpenExternalLinks(True)
        return ret
    
    def __about_line(self, author, year):
        line = "© "
        if isinstance(year, tuple):
            line += "{0}-{1} ".format(year[0], year[1])
        else:
            line += "{0} ".format(author[1])
        line += author
        return line
    
    def __update_started(self, event):
        self.__check_updates.setEnabled(False)

    def __update_finished(self, event):
        self.__update_finished_evt.emit()
