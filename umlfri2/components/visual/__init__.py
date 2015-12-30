from .align import AlignComponent
from .ellipse import EllipseComponent
from .empty import EmptyComponent
from .hbox import HBoxComponent
from .line import LineComponent
from .padding import PaddingComponent
from .rectangle import RectangleComponent
from .shadow import ShadowComponent
from .simple import SimpleComponent
from .sizer import SizerComponent
from .table import TableComponent, TableRow, TableColumn
from .textbox import TextBoxComponent
from .vbox import VBoxComponent

VISUAL_COMPONENTS = {
    'Align': AlignComponent,
    'Ellipse': EllipseComponent,
    'Empty': EmptyComponent,
    'HBox': HBoxComponent,
    'Line': LineComponent,
    'Padding': PaddingComponent,
    'Rectangle': RectangleComponent,
    'Shadow': ShadowComponent,
    'Sizer': SizerComponent,
    'Table': TableComponent,
    'TextBox': TextBoxComponent,
    'VBox': VBoxComponent,
}

TABLE_COMPONENTS = {
    'Row': TableRow,
    'Column': TableColumn,
}

# TODO: components to create: diamond, ellipse, icon, proportional, canvas