from collections import namedtuple
from ..base.component import Component


PointPosition = namedtuple('PointPosition', ('id', 't', 'position', 'orientation'))


class ConnectionLineObject:
    def assign_points(self, points):
        raise NotImplementedError
    
    def draw(self, canvas):
        raise NotImplementedError
    
    def _compute_position(self, points, position):
        old = None
        whole_length = 0
        lengths = []
        first = True
        
        for point in points:
            if first:
                first = False
            else:
                current_length = (point - old).length
                lengths.append(current_length)
                whole_length += current_length
            
            old = point
        
        remaining = position * whole_length
        
        for i, length in enumerate(lengths):
            if remaining < length:
                t = remaining / length

                vector = (points[i + 1] - points[i])
                
                orientation = vector.angle
                point = points[i] + vector * t
                
                return PointPosition(id=i, t=t, position=point, orientation=orientation)
            else:
                remaining -= length
        
        orientation = (points[-1] - points[-2]).angle
        point = points[-1]
        
        return PointPosition(id=len(points)-2, t=1, position=point, orientation=orientation)


class ConnectionLineComponent(Component):
    def _create_object(self, context):
        raise NotImplementedError
    
    def create_connection_object(self, context):
        return self._create_object(context)
