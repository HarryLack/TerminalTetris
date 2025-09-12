
from enum import Enum


class Orientation(Enum):
    NONE = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class Tetronimo(Enum):
    I = 0
    O = 1
    T = 2
    J = 3
    L = 4
    S = 5
    Z = 6


# Offsets
I_STATES = {
    Orientation.NONE: [(0, 1), (1, 1), (2, 1), (3, 1)],
    Orientation.LEFT: [(1, 0), (1, 1), (1, 2), (1, 3)],
    Orientation.DOWN: [(0, 2), (1, 2), (2, 2), (3, 2)],
    Orientation.RIGHT: [(2, 0), (2, 1), (2, 2), (2, 3)]
}
O_STATES = {
    Orientation.NONE: [(0, 0), (0, 1), (1, 0), (1, 1)],
    Orientation.LEFT: [(0, 0), (0, 1), (1, 0), (1, 1)],
    Orientation.DOWN: [(0, 0), (0, 1), (1, 0), (1, 1)],
    Orientation.RIGHT: [(0, 0), (0, 1), (1, 0), (1, 1)]
}
T_STATES = {
    Orientation.NONE: [(0, 0), (0, 1), (0, 2), (1, 1)],
    Orientation.LEFT: [(0, 0), (1, 0), (2, 0), (1, 1)],
    Orientation.DOWN: [(0, 0), (0, 1), (0, 2), (-1, 1)],
    Orientation.RIGHT: [(0, 0), (1, 0), (2, 0), (1, -1)]
}
# TODO
J_STATES = {
    Orientation.NONE: [(0, 0), (0, 1), (0, 2), (0, 3)],
    Orientation.LEFT: [(0, 0), (1, 0), (2, 0), (3, 0)],
    Orientation.DOWN: [(0, 0), (0, 1), (0, 2), (0, 3)],
    Orientation.RIGHT: [(0, 0), (1, 0), (2, 0), (3, 0)]
}
# TODO
L_STATES = {
    Orientation.NONE: [(0, 0), (0, 1), (0, 2), (0, 3)],
    Orientation.LEFT: [(0, 0), (1, 0), (2, 0), (3, 0)],
    Orientation.DOWN: [(0, 0), (0, 1), (0, 2), (0, 3)],
    Orientation.RIGHT: [(0, 0), (1, 0), (2, 0), (3, 0)]
}
# TODO
S_STATES = {
    Orientation.NONE: [(0, 0), (0, 1), (0, 2), (0, 3)],
    Orientation.LEFT: [(0, 0), (1, 0), (2, 0), (3, 0)],
    Orientation.DOWN: [(0, 0), (0, 1), (0, 2), (0, 3)],
    Orientation.RIGHT: [(0, 0), (1, 0), (2, 0), (3, 0)]
}
# TODO
Z_STATES = {
    Orientation.NONE: [(0, 0), (0, 1), (0, 2), (0, 3)],
    Orientation.LEFT: [(0, 0), (1, 0), (2, 0), (3, 0)],
    Orientation.DOWN: [(0, 0), (0, 1), (0, 2), (0, 3)],
    Orientation.RIGHT: [(0, 0), (1, 0), (2, 0), (3, 0)]
}

STATES = {
    Tetronimo.I: I_STATES,
    Tetronimo.O: O_STATES,
    Tetronimo.T: T_STATES,
    Tetronimo.J: J_STATES,
    Tetronimo.L: L_STATES,
    Tetronimo.S: S_STATES,
    Tetronimo.Z: Z_STATES,
}


class Piece:
    def __init__(self, kind: Tetronimo, position: tuple[int], rotation: Orientation = Orientation.NONE):
        self.__kind = kind
        self.__rotation = rotation
        self.__position = position

    @property
    def kind(self):
        return self.__kind

    @property
    def rotation(self):
        return self.__rotation

    @property
    def position(self):
        return self.__position

    def rotate(self, right=True):
        match self.__rotation:
            case Orientation.NONE:
                if right:
                    self.__rotation = Orientation.RIGHT
                else:
                    self.__rotation = Orientation.LEFT
            case Orientation.RIGHT:
                if right:
                    self.__rotation = Orientation.DOWN
                else:
                    self.__rotation = Orientation.NONE
            case Orientation.DOWN:
                if right:
                    self.__rotation = Orientation.LEFT
                else:
                    self.__rotation = Orientation.RIGHT
            case Orientation.LEFT:
                if right:
                    self.__rotation = Orientation.NONE
                else:
                    self.__rotation = Orientation.DOWN

    @property
    def state(self):
        return STATES[self.__kind][self.__rotation]

    def move(self, x: int, y: int):
        self.__position = (self.__position[0]+x, self.__position[1]+y)
