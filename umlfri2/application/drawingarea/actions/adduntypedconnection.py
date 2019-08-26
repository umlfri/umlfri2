from umlfri2.application.commands.diagram.adddiagramconnection import AddDiagramConnectionCommand
from .addconnection import AddConnectionAction


class AddUntypedConnectionAction(AddConnectionAction):
    def __init__(self, source_element):
        super().__init__()
        
        self.__source_element = source_element
    
    def _get_source_element(self, point):
        return self.__source_element
    
    def _create_connection(self, source_element, destination_element, points):
        type = next(self.drawing_area.diagram.parent.project.metamodel.connection_types)
        command = AddDiagramConnectionCommand(
            self.drawing_area.diagram,
            type,
            source_element,
            destination_element,
            points
        )
        self.application.commands.execute(command)
        self.drawing_area.selection.select(command.connection_visual)
        self._finish()
