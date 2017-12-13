from umlfri2.types.threestate import Maybe
from ..base.componenttype import ComponentType
from ..base.helpercomponent import HelperComponent
from umlfri2.types.geometry import Size, Rectangle
from .visualcomponent import VisualComponent, VisualObject


class TableObject(VisualObject):
    def __init__(self, table):
        if table:
            self.__rows = [0] * len(table)
            self.__columns = [0] * max(len(row) for row in table)
        else:
            self.__rows = []
            self.__columns = []
        
        for idrow, row in enumerate(table):
            for idcolumn, child in enumerate(row):
                size = child.get_minimal_size()
                if size.width > self.__columns[idcolumn]:
                    self.__columns[idcolumn] = size.width
                if size.height > self.__rows[idrow]:
                    self.__rows[idrow] = size.height
        
        self.__table = table
    
    def assign_bounds(self, bounds):
        x = bounds.x1
        y = bounds.y1
        
        y_cur = y
        for height, row in zip(self.__rows, self.__table):
            x_cur = x
            for width, child in zip(self.__columns, row):
                child.assign_bounds(Rectangle(x_cur, y_cur, width, height))
                x_cur += width
            y_cur += height
    
    def get_minimal_size(self):
        return Size(sum(self.__columns), sum(self.__rows))
    
    def draw(self, canvas, shadow):
        for row in self.__table:
            for child in row:
                child.draw(canvas, shadow)
    
    def is_resizable(self):
        return Maybe, Maybe


class TableRow(HelperComponent):
    CHILDREN_TYPE = ComponentType.visual
    
    def compile(self, type_context):
        self._compile_children(type_context)


class TableColumn(HelperComponent):
    CHILDREN_TYPE = ComponentType.visual
    
    def compile(self, type_context):
        self._compile_children(type_context)


class TableComponent(VisualComponent):
    CHILDREN_TYPE = ComponentType.table

    def __init__(self, children):
        super().__init__(children)
        
        is_column = None
        
        for child in self._get_semantic_children():
            if isinstance(child, TableRow):
                if is_column is True:
                    raise Exception("Cannot mix rows and columns in a table")
                is_column = False
            elif isinstance(child, TableColumn):
                if is_column is False:
                    raise Exception("Cannot mix rows and columns in a table")
                is_column = True
            else:
                raise Exception("Weird table")
        
        if is_column is None:
            raise Exception("Table contains no row nor column")
        
        self.__is_column = is_column
    
    def _create_object(self, context, ruler):
        ret = []
        
        for local, child in self._get_children(context):
            row = []
            
            for locallocal, localchild in child.get_children(local):
                row.append(localchild._create_object(locallocal, ruler))
            
            ret.append(row)
        
        if self.__is_column:
            return TableObject(list(zip(*ret))) # transpose to get table with rows instead
        else:
            return TableObject(ret)
    
    def compile(self, type_context):
        self._compile_children(type_context)
