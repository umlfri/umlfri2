from .addconnection import AddConnectionAction as AddConnectionAction
from umlfri2.application.commands.diagram.adddiagramconnection import AddDiagramConnectionCommand as AddDiagramConnectionCommand

class AddTypedConnectionAction(AddConnectionAction):
    def __init__(self, type) -> None: ...
    @property
    def connection_type(self): ...
