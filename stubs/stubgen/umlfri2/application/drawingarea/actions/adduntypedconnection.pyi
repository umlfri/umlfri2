from .action import ActionMenuItem as ActionMenuItem
from .addconnection import AddConnectionAction as AddConnectionAction
from umlfri2.application.commands.diagram.adddiagramconnection import AddDiagramConnectionCommand as AddDiagramConnectionCommand

class AddUntypedConnectionAction(AddConnectionAction):
    def __init__(self, source_element) -> None: ...
    @property
    def menu_to_show(self): ...
