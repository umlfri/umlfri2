from ..base.component import Component


class GraphicalObject:
    def assign_bounds(self, bounds):
        raise NotImplementedError

    def draw(self, canvas, shadow):
        raise NotImplementedError


class GraphicalComponent(Component):
    def create_graphical_object(self, context, ruler, size):
        raise NotImplementedError
