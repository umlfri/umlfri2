from ..base.helpercomponent import HelperComponent
from .visualcomponent import VisualComponent, VisualObject


class TableObject(VisualObject):
    def __init__(self, table):
        self.__rows = [0] * len(table)
        self.__columns = [0] * max(len(row) for row in table)
        
        for idrow, row in enumerate(table):
            for idcolumn, child in enumerate(row):
                w, h = child.get_minimal_size()
                if w > self.__columns[idcolumn]:
                    self.__columns[idcolumn] = w
                if h > self.__rows[idrow]:
                    self.__rows[idrow] = h
        
        self.__table = table
    
    def assign_bounds(self, bounds):
        x, y, w, h = bounds
        
        y_cur = y
        for height, row in zip(self.__rows, self.__table):
            x_cur = x
            for width, child in zip(self.__columns, row):
                child.assign_bounds((x_cur, y_cur, width, height))
                x_cur += width
            y_cur += height
    
    def get_minimal_size(self):
        return sum(self.__columns), sum(self.__rows)
    
    def draw(self, canvas, shadow):
        for row in self.__table:
            for child in row:
                child.draw(canvas, shadow)


class TableRow(HelperComponent):
    pass


class TableColumn(HelperComponent):
    pass


class Table(VisualComponent):
    def _create_object(self, context, ruler):
        iscolumn = False # is this table with columns?
        ret = []
        
        for local, child in self._get_children(context):
            if isinstance(child, TableColumn):
                iscolumn = True
            
            row = []
            
            for locallocal, localchild in child.get_children(local):
                row.append(localchild._create_object(locallocal, ruler))
            
            ret.append(row)
        
        if iscolumn:
            return TableObject(list(zip(*ret))) # transpose to get table with rows instead
        else:
            return TableObject(ret)
