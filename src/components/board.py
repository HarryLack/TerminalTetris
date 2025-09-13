import curses
from functools import reduce
from components.piece import Piece
from components.tile import Tile, TileType
from keys import Key
from logger import Logger


def x_reducer(acc: list, val: tuple[int, int]):
    acc.append(val[0])
    return acc


def y_reducer(acc: list, val: tuple[int, int]):
    acc.append(val[1])
    return acc


class Board:
    def __init__(self, width, height, offset=0, logger: Logger | None = None):
        if logger is not None:
            self.__logger = logger.append("[Board]")
        else:
            self.__logger = Logger(prefix="[Board]")

        self.__active_piece: Piece | None = None
        self.__width = width
        self.__height = height
        self.__offset = offset
        self.__tiles: list[list[Tile]] = [[Tile(TileType.Empty) for _ in range(width)]
                                          for _ in range(height)]
        self.__board = [[Tile(TileType.Empty) for _ in range(width)]
                        for _ in range(height)]
        self.__setup_tiles()

    def __setup_tiles(self):
        for i in range(self.__height):
            for j in range(self.__width):
                self.__board[i][j] = Tile(TileType.Empty)

    def __render_piece(self):
        if not self.__active_piece:
            return

        for (x, y) in self.__active_piece.position:
            self.__board[y][x] = Tile(TileType.Piece)

    def __render_tiles(self):
        for y, row in enumerate(self.__tiles):
            for x, tile in enumerate(row):
                self.__board[y][x] = tile

    def __store_piece(self):
        pass

    def __move_left(self):
        if self.__active_piece is None:
            return

        min_x = min(reduce(x_reducer, self.__active_piece.position, []))
        if min_x <= 0:
            return False

        self.__logger.log("moving left")
        self.__active_piece.move(-1, 0)

    def __move_right(self):
        if self.__active_piece is None:
            return

        max_x = max(reduce(x_reducer, self.__active_piece.position, []))
        if max_x >= self.__width-1:
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
        max_y = max(reduce(y_reducer, self.__active_piece.position, []))
        self.__logger.log(f"max_y: {max_y}")
        if max_y >= self.__height-1:
            return False

        self.__logger.log("moving down")
        self.__active_piece.move(0, 1)

        is_stopped = False

        for (pos_x, pos_y) in self.__active_piece.position:
            if pos_y >= self.__height-1:
                is_stopped = True
                break

            below = self.__tiles[pos_y+1][pos_x]
            if below.symbol is not TileType.Empty:
                self.__logger.log("should stop")

        if is_stopped:
            self.__store_piece()

    def __drop(self):
        if self.__active_piece is None:
            return

        max_y = max(reduce(y_reducer, self.__active_piece.position, []))

        diff = self.__height-1 - max_y

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
