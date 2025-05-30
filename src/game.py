import curses
from enum import Enum
import time

from constants import SCALE, TARGET_FRAME_TIME
from logger import Logger


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
    Orientation.NONE: [(0, 0), (0, 1), (0, 2), (0, 3)],
    Orientation.LEFT: [(0, 0), (1, 0), (2, 0), (3, 0)],
    Orientation.DOWN: [(0, 0), (0, 1), (0, 2), (0, 3)],
    Orientation.RIGHT: [(0, 0), (1, 0), (2, 0), (3, 0)]
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


class Tile:
    def __init__(self, symbol: str):
        self.__symbol = symbol[0]

    def render(self):
        return self.__symbol


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

    def move(self, x, y):
        self.__position = (self.__position[0]+x, self.__position[1]+y)


class Board:
    def __init__(self, width, height):
        self.__active_piece: Piece | None = None
        self.__pieces: list[Piece] = []
        self.__width = width
        self.__height = height
        self.__board = [[Tile(" ") for _ in range(width)]
                        for _ in range(height)]
        self.__reset_board()

    def __reset_board(self):
        for i in range(self.__height):
            for j in range(self.__width):
                if i == 0 or i == self.__height-1 or j == 0 or j == self.__width-1:
                    self.__board[i][j] = Tile("#")
                else:
                    self.__board[i][j] = Tile(" ")

    def __render_pieces(self):
        for piece in self.__pieces:
            for (y, x) in piece.state:
                self.__board[y+piece.position[1]][x+piece.position[0]] = Tile("@")

    @property
    def active_piece(self):
        return self.__active_piece

    @property
    def pieces(self):
        return self.__pieces

    def add_piece(self, piece: Piece):
        if self.__active_piece is not None:
            return ValueError("add_piece called while piece still in play")
        self.__active_piece = piece
        self.__pieces.append(piece)
        return True

    def render(self):
        self.__reset_board()
        self.__render_pieces()
        world = ""
        for row in self.__board:
            for col in row:
                world += col.render()
            world += "\n"
        return world


class GameController:
    def __init__(self, screen: curses.window, width, height, logger=Logger()):
        self.__screen = screen
        self.__board = Board(width=width*SCALE, height=height*SCALE)
        self.__logger = logger

    def render(self):
        res = ""
        res += self.__board.render()
        return res

    def piece(self):
        pass

    def tick(self):
        pass

    def action(self):
        # TODO Make this actually game loop
        key = self.__screen.getch()
        self.__logger.log(f"Key:{key}")
        match key:
            # w
            case 119:
                self.__logger.log("w")
            # s
            case 115:
                self.__logger.log("s")
            # a
            case 97:
                self.__logger.log("a")
            # d
            case 100:
                self.__logger.log("d")
            # q
            case 113:
                self.__logger.log("q")
            # ESC
            case 27:
                self.__logger.log("esc")
                curses.endwin()
                return

    def update(self, dt: float):
        if not self.__board.active_piece:
            self.__board.add_piece(Piece(kind=Tetronimo.I, position=(1, 1)))
        pass

    def draw(self):
        self.__screen.addstr(0, 0, self.render())
        self.__screen.addstr(f"{iter}")
        self.__screen.move(curses.LINES-1, curses.COLS - 1)
        self.__screen.refresh()

    def play(self):
        dt = time.time()

        iter = 0
        while (True and iter < 1000):
            self.action()
            self.update(dt)

            iter += 1
            now = time.time()
            if (now - dt) < TARGET_FRAME_TIME:
                time.sleep(TARGET_FRAME_TIME-(now-dt))
                continue

            self.draw()

            dt = now
            self.tick()
