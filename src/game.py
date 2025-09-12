import curses
import time

from components.board import Board
from components.border import Border
from components.piece import Piece, Tetronimo
from constants import BORDER_WIDTH, SCALE, TARGET_FRAME_TIME
from errors import ScreenSizeException
from logger import Logger


class GameController:
    def __init__(self, screen: curses.window, width, height, logger=Logger(prefix="[GameController]: ")):
        (screen_height, screen_width) = screen.getmaxyx()
        if screen_height < height or screen_width < width:
            raise ScreenSizeException(
                f"screen w:{screen_width} h:{screen_height} below required size w:{width} h:{height}")

        self.__screen = screen
        self.__border = Border(
            width=width*SCALE, height=height*SCALE, size=BORDER_WIDTH*SCALE)
        self.__board = Board(
            width=width*SCALE, height=height*SCALE, offset=BORDER_WIDTH*SCALE, logger=logger)
        self.__logger = logger

    def piece(self):
        pass

    def tick(self):
        pass

    def action(self):
        # TODO: Make this actually game loop
        key = self.__screen.getch()
        self.__logger.log(f"Key:{key}")
        # TODO: Vim keys
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
                # self.__board.active_piece.move(-1,0)
            # d
            case 100:
                self.__logger.log("d")
                # self.__board.active_piece.move(1,0)
            # q
            case 113:
                self.__logger.log("q")
            # ESC
            case 27:
                self.__logger.log("esc")
                curses.endwin()
                quit()
                return
        self.__board.action(key)

    def update(self, dt: float):
        if not self.__board.active_piece:
            self.__board.add_piece(Piece(kind=Tetronimo.I, position=(1, 1)))
        pass

    def draw(self):
        self.__border.render(self.__screen)
        self.__board.render(self.__screen)
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
