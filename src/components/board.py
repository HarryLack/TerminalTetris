import curses
from functools import reduce
from components.piece import Piece
from components.tile import Tile
from keys import Key
from logger import Logger


def x_reducer(acc: list, val: tuple[int, int]):
    acc.append(val[0])
    return acc


def y_reducer(acc: list, val: tuple[int, int]):
    acc.append(val[1])
    return acc


class Board:
    def __init__(self, width, height, offset, logger=Logger(prefix="Board")):
        self.__logger = logger
        self.__active_piece: Piece | None = None
        self.__width = width
        self.__height = height
        self.__offset = offset
        self.__tiles: list[list[Tile]] = [[Tile(" ") for _ in range(width)]
                                          for _ in range(height)]
        self.__board = [[Tile(" ") for _ in range(width)]
                        for _ in range(height)]
        self.__setup_tiles()

    def __setup_tiles(self):
        for i in range(self.__height):
            for j in range(self.__width):
                self.__tiles[i][j] = Tile(" ")

    def __render_piece(self):
        if not self.__active_piece:
            return

        for (x, y) in self.__active_piece.state:
            self.__board[y+self.__active_piece.position[1]][x +
                                                            self.__active_piece.position[0]] = Tile("@")

    def __render_tiles(self):
        for y, row in enumerate(self.__tiles):
            for x, tile in enumerate(row):
                self.__board[y][x] = tile

    def __move_left(self):
        if self.__active_piece is None:
            return

        x = reduce(x_reducer, self.__active_piece.state, [])
        min_x = min(x)+self.__active_piece.position[0]
        if min_x <= 1:
            return False

        self.__logger.log("moving left")
        self.__active_piece.move(-1, 0)

    def __move_right(self):
        if self.__active_piece is None:
            return

        x = reduce(x_reducer, self.__active_piece.state, [])

        max_x = max(x)+self.__active_piece.position[0]
        if max_x >= self.__width-2:
            return False

        self.__logger.log("moving right")
        self.__active_piece.move(1, 0)

    def __rotate_right(self):
        if self.__active_piece is None:
            return

        self.__active_piece.rotate(True)

    def __rotate_left(self):
        if self.__active_piece is None:
            return

        self.__active_piece.rotate()

    def __down(self):
        if self.__active_piece is None:
            return

        # TODO:
        y = reduce(y_reducer, self.__active_piece.state, [])
        max_y = max(y) + self.__active_piece.position[1]

        if max_y >= self.__height-2:
            return False

        self.__logger.log("moving down")
        self.__active_piece.move(0, 1)

    def __drop(self):
        if self.__active_piece is None:
            return

        y = reduce(y_reducer, self.__active_piece.state, [])
        max_y = max(y) + self.__active_piece.position[1]

        diff = self.__height-2 - max_y

        self.__logger.log("dropping")
        self.__active_piece.move(0, diff)

    def action(self, key_code: int):
        match key_code:
            case Key.w.value:
                self.__logger.log("w")
                self.__drop()
            case Key.s.value:
                self.__logger.log("s")
                self.__down()
            case Key.a.value:
                self.__logger.log("a")
                self.__move_left()
            case Key.d.value:
                self.__logger.log("d")
                self.__move_right()
            case Key.q.value:
                self.__logger.log("q")
                self.__rotate_left()
            case Key.e.value:
                self.__logger.log("e")
                self.__rotate_right()
            case _:
                self.__logger.log(f"Code:{key_code} | Key:{chr(key_code)}")

    @property
    def active_piece(self):
        return self.__active_piece

    def add_piece(self, piece: Piece):
        if self.__active_piece is not None:
            return ValueError("add_piece called while piece still in play")
        self.__active_piece = piece
        return True

    def render(self, screen: curses.window):
        self.__logger.log("Rendering")
        self.__render_tiles()
        self.__render_piece()

        for row_idx, row in enumerate(self.__board):
            for col_idx, col in enumerate(row):
                screen.addstr(self.__offset+row_idx,
                              self.__offset+col_idx, col.render())
