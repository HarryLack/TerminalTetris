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
    Orientation.NONE: [[0, 0], [0, 1], [0, 2], [0, 3]],
    Orientation.LEFT: [[0, 0], [1, 0], [2, 0], [3, 0]],
    Orientation.DOWN: [[0, 0], [0, 1], [0, 2], [0, 3]],
    Orientation.RIGHT: [[0, 0], [1, 0], [2, 0], [3, 0]]
}
O_STATES = {
    Orientation.NONE: [[0, 0], [0, 1], [1, 0], [1, 1]],
    Orientation.LEFT: [[0, 0], [0, 1], [1, 0], [1, 1]],
    Orientation.DOWN: [[0, 0], [0, 1], [1, 0], [1, 1]],
    Orientation.RIGHT: [[0, 0], [0, 1], [1, 0], [1, 1]]
}
T_STATES = {
    Orientation.NONE: [[0, 0], [0, 1], [0, 2], [1, 1]],
    Orientation.LEFT: [[0, 0], [1, 0], [2, 0], [1, 1]],
    Orientation.DOWN: [[0, 0], [0, 1], [0, 2], [-1, 1]],
    Orientation.RIGHT: [[0, 0], [1, 0], [2, 0], [1, -1]]
}
# TODO
J_STATES = {
    Orientation.NONE: [[0, 0], [0, 1], [0, 2], [0, 3]],
    Orientation.LEFT: [[0, 0], [1, 0], [2, 0], [3, 0]],
    Orientation.DOWN: [[0, 0], [0, 1], [0, 2], [0, 3]],
    Orientation.RIGHT: [[0, 0], [1, 0], [2, 0], [3, 0]]
}
# TODO
L_STATES = {
    Orientation.NONE: [[0, 0], [0, 1], [0, 2], [0, 3]],
    Orientation.LEFT: [[0, 0], [1, 0], [2, 0], [3, 0]],
    Orientation.DOWN: [[0, 0], [0, 1], [0, 2], [0, 3]],
    Orientation.RIGHT: [[0, 0], [1, 0], [2, 0], [3, 0]]
}
# TODO
S_STATES = {
    Orientation.NONE: [[0, 0], [0, 1], [0, 2], [0, 3]],
    Orientation.LEFT: [[0, 0], [1, 0], [2, 0], [3, 0]],
    Orientation.DOWN: [[0, 0], [0, 1], [0, 2], [0, 3]],
    Orientation.RIGHT: [[0, 0], [1, 0], [2, 0], [3, 0]]
}
# TODO
Z_STATES = {
    Orientation.NONE: [[0, 0], [0, 1], [0, 2], [0, 3]],
    Orientation.LEFT: [[0, 0], [1, 0], [2, 0], [3, 0]],
    Orientation.DOWN: [[0, 0], [0, 1], [0, 2], [0, 3]],
    Orientation.RIGHT: [[0, 0], [1, 0], [2, 0], [3, 0]]
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
    def __init__(self, kind: Tetronimo, rotation: Orientation):
        self.__kind = kind
        self.__rotation = rotation
        pass

    @property
    def kind(self):
        return self.__kind

    @property
    def rotation(self):
        return self.__rotation

    # TODO Check this?
    def rotate(self, right=True):
        self.__rotation -= 1

    # Rename this?
    def rep(self):
        return STATES[self.__kind][self.rotation]


class Board:
    def __init__(self):
        self.__pieces: list[Tetronimo] = []
        pass
