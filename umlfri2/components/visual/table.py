from ..base.helpercomponent import HelperComponent
from .visualcomponent import VisualComponent


class TableRow(HelperComponent):
    pass


class TableColumn(HelperComponent):
    pass


class Table(VisualComponent):
    def __get_table(self, context):
        iscolumn = False # is this table with columns?
        ret = []
        
        for local, child in self._get_children(context):
            if isinstance(child, TableColumn):
                iscolumn = True
            
            ret.append(list(child.get_children(local)))
        
        if iscolumn:
            return zip(*ret) # transpose to get table with rows instead
        else:
            return ret
    
    def __compute_sizes(self, table, ruler):
        rows = [0] * len(table)
        columns = [0] * max(len(row) for row in table)
        
        for idrow, row in enumerate(table):
            for idcolumn, (local, child) in enumerate(row):
                w, h = child.get_size(local, ruler)
                if w > columns[idcolumn]:
                    columns[idcolumn] = w
                if h > rows[idrow]:
                    rows[idrow] = h
        
        return columns, rows
    
    def get_size(self, context, ruler):
        columns, rows = self.__compute_sizes(self.__get_table(context), ruler)
        return sum(columns), sum(rows)
    
    def draw(self, context, canvas, bounds, shadow=None):
        x, y, w, h = bounds
        
        table = self.__get_table(context)
        columns, rows = self.__compute_sizes(table, canvas.get_ruler())
        
        y_cur = y
        for height, row in zip(rows, table):
            x_cur = x
            for width, (local, child) in zip(columns, row):
                child.draw(context, canvas, (x_cur, y_cur, width, height), shadow)
                x_cur += width
            y_cur += height
