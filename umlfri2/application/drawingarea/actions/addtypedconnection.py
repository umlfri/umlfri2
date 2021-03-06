from umlfri2.application.commands.diagram.adddiagramconnection import AddDiagramConnectionCommand
from .addconnection import AddConnectionAction


class AddTypedConnectionAction(AddConnectionAction):
    def __init__(self, type):
        super().__init__()
        self.__type = type
    
    @property
    def connection_type(self):
        return self.__type
    
    def _get_source_element(self, point):
        return self.drawing_area.diagram.get_visual_at(self.application.ruler, point)
    
    def _create_connection(self, source_element, destination_element, points):
        type = self.drawing_area.diagram.parent.project.metamodel.get_connection_type(self.__type)
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
