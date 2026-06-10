from .tabletab import TableTab as TableTab

class EmptyTab(TableTab):
    @property
    def label(self): ...
