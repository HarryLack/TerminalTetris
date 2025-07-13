from functools import reduce
from components.piece import Piece
from components.tile import Tile
from logger import Logger


def x_reducer(acc: list, val: tuple[int, int]):
    acc.append(val[0])
    return acc


class Board:
    def __init__(self, width, height, logger=Logger(prefix="Board")):
        self.__logger = logger
        self.__active_piece: Piece | None = None
        self.__width = width
        self.__height = height
        self.__tiles: list[list[Tile]] = [[Tile(" ") for _ in range(width)]
                                          for _ in range(height)]
        self.__board = [[Tile(" ") for _ in range(width)]
                        for _ in range(height)]
        self.__setup_tiles()

    def __setup_tiles(self):
        for i in range(self.__height):
            for j in range(self.__width):
                if i == 0 or i == self.__height-1 or j == 0 or j == self.__width-1:
                    self.__tiles[i][j] = Tile("#")
                else:
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

    def action(self, key_code: int):
        match key_code:
            # w
            case 119:
                self.__logger.log("w")
            # s
            case 115:
                self.__logger.log("s")
            # a
            case 97:
                self.__logger.log("a")
                self.__move_left()
            # d
            case 100:
                self.__logger.log("d")
                self.__move_right()
            # q
            case 113:
                self.__logger.log("q")

    @property
    def active_piece(self):
        return self.__active_piece

    def add_piece(self, piece: Piece):
        if self.__active_piece is not None:
            return ValueError("add_piece called while piece still in play")
        self.__active_piece = piece
        return True

    def render(self):
        self.__logger.log("Rendering")
        self.__render_tiles()
        self.__render_piece()

        world = ""
        for row in self.__board:
            for col in row:
                world += col.render()
            world += "\n"
        return world
