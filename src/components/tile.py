
class Tile:
    def __init__(self, symbol: str):
        self.__symbol = symbol[0]

    def render(self):
        return self.__symbol
