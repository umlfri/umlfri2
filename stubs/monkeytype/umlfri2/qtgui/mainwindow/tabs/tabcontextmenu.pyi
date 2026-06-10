from umlfri2.qtgui.canvas.scrolledcanvaswidget import ScrolledCanvasWidget
from umlfri2.qtgui.mainwindow.tabs.tabbar import MiddleClosableTabBar


class TabContextMenu:
    def __init__(
        self,
        tab_bar: MiddleClosableTabBar,
        tab_index: int,
        tab_widget: ScrolledCanvasWidget
    ) -> None: ...
