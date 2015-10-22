from collections import namedtuple
import math
from ..base.component import Component


PointPosition = namedtuple('PointPosition', ('id', 't', 'position', 'orientation'))


class ConnectionLineObject:
    def assign_points(self, points):
        raise NotImplementedError
    
    def draw(self, canvas):
        raise NotImplementedError
    
    def _compute_position(self, points, position):
        old_x, old_y = None, None
        whole_length = 0
        lengths = []
        first = True
        
        for x, y in points:
            if first:
                first = False
            else:
                current_length = math.sqrt((old_x - x)**2 + (old_y - y)**2)
                lengths.append(current_length)
                whole_length += current_length
            
            old_x = x
            old_y = y
        
        remaining = position * whole_length
        
        for i, length in enumerate(lengths):
            if remaining < length:
                t = remaining / length
                
                x1, y1 = points[i]
                x2, y2 = points[i + 1]
                
                orientation = math.atan2(y2 - y1, x2 - x1)
                point = int(round(x2*t + x1*(1-t))), int(round(y2*t + y1*(1-t)))
                
                return PointPosition(id=i, t=t, position=point, orientation=orientation)
            else:
                remaining -= length
        
        x1, y1 = points[-2]
        x2, y2 = points[-1]
        
        orientation = math.atan2(y2 - y1, x2 - x1)
        point = x2, y2
        
        return PointPosition(id=len(points)-2, t=1, position=point, orientation=orientation)


class ConnectionLineComponent(Component):
    def is_control(self):
        return False
    
    def _create_object(self, context):
        raise NotImplementedError
    
    def create_connection_object(self, context):
        return self._create_object(context)
