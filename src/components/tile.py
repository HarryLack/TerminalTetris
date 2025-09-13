
from enum import Enum


class TileType(Enum):
    Empty = "_"
    Border = "#"
    Piece = "@"


class Tile:
    def __init__(self, symbol: TileType):
        self.__symbol = symbol

    @property
    def symbol(self):
        return self.__symbol

    def render(self):
        return self.__symbol.value
