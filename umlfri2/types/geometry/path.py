from .vector import Vector
from .point import Point


class PathCommand:
    def __init__(self, final_point):
        self.__final_point = final_point
    
    @property
    def final_point(self):
        return self.__final_point
    
    def __str__(self):
        raise NotImplementedError
    
    def __repr__(self):
        raise NotImplementedError
    
    def transform(self, matrix):
        raise NotImplementedError


class PathLineTo(PathCommand):
    def __str__(self):
        return "L {0}".format(self.final_point)
    
    def __repr__(self):
        return "<PathLineTo {0}>".format(self.final_point)
    
    def transform(self, matrix):
        return PathLineTo(self.final_point.transform(matrix))


class PathCubicTo(PathCommand):
    def __init__(self, control_point1, control_point2, final_point):
        super().__init__(final_point)
        self.__control_point1 = control_point1
        self.__control_point2 = control_point2
    
    @property
    def control_point1(self):
        return self.__control_point1
    
    @property
    def control_point2(self):
        return self.__control_point2
    
    def __str__(self):
        return "C {0} {1} {2}".format(self.__control_point1,
                                      self.__control_point2, self.final_point)
    
    def __repr__(self):
        return "<PathCubicTo {0} {1} {2}>".format(self.__control_point1,
                                                  self.__control_point2, self.final_point)
    
    def transform(self, matrix):
        return PathCubicTo(self.__control_point1.transform(matrix),
                           self.__control_point2.transform(matrix),
                           self.final_point.transform(matrix))


class PathSegment:
    def __init__(self, starting_point, commands, closed=False):
        self.__starting_point = starting_point
        self.__commands = tuple(commands)
        self.__closed = closed
    
    @property
    def starting_point(self):
        return self.__starting_point
    
    @property
    def commands(self):
        return self.__commands
    
    @property
    def closed(self):
        return self.__closed
    
    def __str__(self):
        if self.__closed:
            format = "M {0} {1} z"
        else:
            format = "M {0} {1}"
        
        return format.format(self.__starting_point, " ".join(str(i) for i in self.__commands))
    
    def __repr__(self):
        return "<PathSegment {0} [{1}] {2}>".format(self.__starting_point,
                                                    " ".join(str(i) for i in self.__commands),
                                                    self.__closed)
    
    def transform(self, matrix):
        new_commands = [command.transform(matrix) for command in self.__commands]
        return PathSegment(self.__starting_point.transform(matrix), new_commands, self.__closed)


class Path:
    def __init__(self, segments):
        self.__segments = tuple(segments)
    
    @property
    def segments(self):
        return self.__segments
    
    def __str__(self):
        return " ".join(str(i) for i in self.__segments)
    
    def __repr__(self):
        return "<Path [{0}]>".format(" ".join(str(i) for i in self.__segments))
    
    def transform(self, matrix):
        new_segments = [segment.transform(matrix) for segment in self.__segments]
        return Path(new_segments)


class PathBuilder:
    def __init__(self):
        self.__commands = []
        self.__origin = None
        self.__segments = []
        self.__last = Point(0, 0)
    
    def build(self):
        if self.__origin and self.__commands:
            self.__segments.append(PathSegment(self.__origin, self.__commands))
            self.__commands = []
        
        return Path(self.__segments)

    def __recalculate(self, *points):
        last = self.__last
        
        for point in points:
            ret = point
            if isinstance(point, Vector):
                ret = last + ret
            self.__last = ret
            yield ret
    
    def move_to(self, point):
        if self.__origin and self.__commands:
            self.__segments.append(PathSegment(self.__origin, self.__commands))
            self.__commands = []
        
        point, = self.__recalculate(point)
        
        self.__origin = point
        
        return self
            
    def line_to(self, point):
        point, = self.__recalculate(point)
        self.__commands.append(PathLineTo(point))
        
        return self
    
    def cubic_to(self, control1, control2, point):
        control1, control2, point = self.__recalculate(control1, control2, point)
        
        self.__commands.append(PathCubicTo(control1, control2, point))
        
        return self
    
    def close(self):
        if self.__origin and self.__commands:
            self.__segments.append(PathSegment(self.__origin, self.__commands, True))
            self.__commands = []
        
        self.__last = self.__origin
        
        return self
    
    def from_string(self, s):
        cmds = s.replace(',', ' ').split()
        cur = None
        
        pop_point = lambda: Point(float(cmds.pop(0)), float(cmds.pop(0)))
        pop_vector = lambda: Vector(float(cmds.pop(0)), float(cmds.pop(0)))
        
        while cmds:
            if cmds[0].isalpha():
                cur = cmds.pop(0)
            
            if cur == 'M':
                cur = 'L'
                self.move_to(pop_point())
            elif cur == 'm':
                cur = 'l'
                self.move_to(pop_vector())
            elif cur == 'L':
                self.line_to(pop_point())
            elif cur == 'l':
                self.line_to(pop_vector())
            elif cur == 'C':
                self.cubic_to(pop_point(), pop_point(), pop_point())
            elif cur == 'c':
                self.cubic_to(pop_vector(), pop_vector(), pop_vector())
            elif cur in 'zZ':
                self.close()
            else:
                raise Exception
        
        return self
