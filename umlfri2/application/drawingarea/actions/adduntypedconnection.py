from functools import partial

from umlfri2.application.commands.diagram.adddiagramconnection import AddDiagramConnectionCommand
from .addconnection import AddConnectionAction
from .action import ActionMenuItem


class AddUntypedConnectionAction(AddConnectionAction):
    def __init__(self, source_element):
        super().__init__()
        
        self.__source_element = source_element
        self.__connections_menu = None
    
    @property
    def menu_to_show(self):
        return self.__connections_menu
    
    def _get_source_element(self, point):
        return self.__source_element
    
    def _create_connection(self, source_element, destination_element, points):
        metamodel = self.drawing_area.diagram.parent.project.metamodel
        diagram_type = self.drawing_area.diagram.type
        translation = metamodel.get_translation(self.application.language.current_language)
        self.__connections_menu = []
        for connection_type in diagram_type.connection_types:
            self.__connections_menu.append(
                ActionMenuItem(
                    connection_type.icon,
                    translation.translate(connection_type),
                    partial(self.__create_connection_finish, source_element, destination_element, points, connection_type)
                )
            )
    
    def __create_connection_finish(self, source_element, destination_element, points, type):
        self.__connections_menu = None
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
