from enum import Enum, unique


@unique
class DrawingAreaCursor(Enum):
    arrow = 1
    move = 2
    main_diagonal_resize = 3
    anti_diagonal_resize = 4
    horizontal_resize = 5
    vertical_resize = 6
    cross = 7
