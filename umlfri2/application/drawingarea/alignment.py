from collections import namedtuple

from umlfri2.types.geometry import Point


Aligned = namedtuple("Aligned", ["result", "horizontal_indicators", "vertical_indicators"])


class Alignment:
    MAXIMAL_DISTANCE = 10
    
    def __init__(self, rectangles, points):
        self.__center_guidelines = []
        self.__vertical_guidelines = []
        self.__horizontal_guidelines = []
        
        self.__center_guidelines.extend(points)
        
        for rectangle in rectangles:
            self.__center_guidelines.append(rectangle.center)
            self.__vertical_guidelines.append(rectangle.top_center)
            self.__vertical_guidelines.append(rectangle.bottom_center)
            self.__horizontal_guidelines.append(rectangle.left_center)
            self.__horizontal_guidelines.append(rectangle.right_center)
    
    def add_point(self, point):
        self.__center_guidelines.append(point)
    
    def ignore_point(self, point):
        if point in self.__center_guidelines:
            self.__center_guidelines.remove(point)
    
    def align_point(self, point):
        best_horizontal = None
        best_horizontal_distance = self.MAXIMAL_DISTANCE
        best_vertical = None
        best_vertical_distance = self.MAXIMAL_DISTANCE
        
        for guideline in self.__center_guidelines:
            horizontal_distance = abs(guideline.x - point.x)
            vertical_distance = abs(guideline.y - point.y)
            if horizontal_distance < best_horizontal_distance:
                best_horizontal_distance = horizontal_distance
                best_horizontal = guideline
            if vertical_distance < best_vertical_distance:
                best_vertical_distance = vertical_distance
                best_vertical = guideline
        
        horizontal_indicators = set()
        vertical_indicators = set()
        
        if best_horizontal is not None and best_vertical is not None:
            point = Point(best_horizontal.x, best_vertical.y)
        elif best_horizontal is not None:
            point = Point(best_horizontal.x, point.y)
        elif best_vertical is not None:
            point = Point(point.x, best_vertical.y)
        
        if best_horizontal is not None:
            for guideline in self.__center_guidelines:
                if best_horizontal.x == guideline.x:
                    horizontal_indicators.add(guideline)
            horizontal_indicators.add(point)
        
        if best_vertical is not None:
            for guideline in self.__center_guidelines:
                if best_vertical.y == guideline.y:
                    vertical_indicators.add(guideline)
            vertical_indicators.add(point)
        
        return Aligned(
            point,
            sorted(horizontal_indicators, key=lambda item: item.x),
            sorted(vertical_indicators, key=lambda item: item.y)
        )
