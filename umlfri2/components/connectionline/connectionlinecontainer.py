from .connectionlinecomponent import ConnectionLineComponent, ConnectionLineObject


class ConnectionLineContainerObject(ConnectionLineObject):
    def __init__(self, children):
        self.__children = list(children)
    
    def assign_points(self, points):
        for child in self.__children:
            child.assign_points(points)
    
    def draw(self, canvas):
        for child in self.__children:
            child.draw(canvas)


class ConnectionLineContainerComponent(ConnectionLineComponent):
    def _create_object(self, context):
        return ConnectionLineContainerObject(self._get_children(context))
