from .align import AlignComponent
from .hbox import HBoxComponent
from .line import LineComponent
from .padding import PaddingComponent
from .rectangle import RectangleComponent
from .shadow import ShadowComponent
from .table import TableComponent, TableRow, TableColumn
from .textbox import TextBoxComponent
from .vbox import VBoxComponent

VISUAL_COMPONENTS = {
    'Align': AlignComponent,
    'HBox': HBoxComponent,
    'Line': LineComponent,
    'Padding': PaddingComponent,
    'Rectangle': RectangleComponent,
    'Shadow': ShadowComponent,
    'Table': TableComponent,
    'Row': TableRow,
    'Column': TableColumn,
    'TextBox': TextBoxComponent,
    'VBox': VBoxComponent,
}
