from .align import Align
from .hbox import HBox
from .line import Line
from .padding import Padding
from .rectangle import Rectangle
from .shadow import Shadow
from .table import Table, TableRow, TableColumn
from .textbox import TextBox
from .vbox import VBox

VISUAL_COMPONENTS = {
    'Align': Align,
    'HBox': HBox,
    'Line': Line,
    'Padding': Padding,
    'Rectangle': Rectangle,
    'Shadow': Shadow,
    'Table': Table,
    'Row': TableRow,
    'Column': TableColumn,
    'TextBox': TextBox,
    'VBox': VBox,
}
