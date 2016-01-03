from .tabletab import TableTab


class EmptyTab(TableTab):
    @property
    def label(self):
        return _("General")
