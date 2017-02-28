from .align import AlignComponent
from .diamond import DiamondComponent
from .ellipse import EllipseComponent
from .empty import EmptyComponent
from .graphics import GraphicsComponent
from .hbox import HBoxComponent
from .image import ImageComponent
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
    'Diamond': DiamondComponent,
    'Ellipse': EllipseComponent,
    'Empty': EmptyComponent,
    'Graphics': GraphicsComponent,
    'HBox': HBoxComponent,
    'Image': ImageComponent,
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
