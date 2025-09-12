import curses
from components.tile import Tile


class Border:
    def __init__(self, width: int, height: int, size: int):
        self.__tiles: list[list[Tile]] = [[Tile("#") for _ in range(width+(size*2))]
                                          for _ in range(height+(size*2))]

    @property
    def tiles(self):
        return self.__tiles

    def render(self, screen: curses.window):
        for row_idx, row in enumerate(self.__tiles):
            for col_idx, col in enumerate(row):
                screen.addstr(row_idx, col_idx, col.render())
