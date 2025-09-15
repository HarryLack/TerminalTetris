import curses
import sys
import time

from components.board import Board
from components.border import Border
from components.piece import Piece, Tetronimo
from constants import BORDER_WIDTH, SCALE, TARGET_FRAME_RATE, TARGET_FRAME_TIME, TARGET_TICK_RATE
from errors import ScreenSizeException
from keys import Key
from logger import Logger


class GameController:
    def __init__(self, screen: curses.window, width, height, logger: Logger | None = None):
        (screen_height, screen_width) = screen.getmaxyx()
        if screen_height < height or screen_width < width:
            raise ScreenSizeException(
                f"screen w:{screen_width} h:{screen_height} below required size w:{width} h:{height}")

        if logger is not None:
            self.__logger = logger.append("[GameController]")
        else:
            self.__logger = Logger(prefix="[GameController]")

        self.__screen = screen
        self.__border = Border(
            width=width*SCALE, height=height*SCALE, size=BORDER_WIDTH*SCALE)
        self.__board = Board(
            width=width*SCALE, height=height*SCALE, offset=BORDER_WIDTH*SCALE, logger=self.__logger)

        self.last_drop = time.time()

        self.__logger.log(f"{GameController.__name__} init")

    def piece(self):
        pass

    def tick(self):
        pass

    def action(self):
        # TODO: Make this actually game loop
        key = self.__screen.getch()
        self.__logger.log(f"Key:{key}")
        # TODO: Vim keys?
        match key:
            case Key.s.value:
                self.last_drop = time.time()
            # ESC
            case Key.ESC.value:
                self.__logger.log("esc")
                curses.endwin()
                sys.exit()
            case -1:
                # No input case
                pass
            case _:
                self.__logger.log(f"Code:{key} | Key:{chr(key)}")
        self.__board.action(key)

    def update(self, dt: float):
        if not self.__board.active_piece:
            self.__board.add_piece(Piece(kind=Tetronimo.I, position=(1, 1)))

        now = time.time()
        if (now - self.last_drop) > TARGET_TICK_RATE:
            self.__logger.log("timeout")
            # TODO: not this
            self.__board.action(Key.s.value)
            self.last_drop = now

    def draw(self):
        self.__border.render(self.__screen)
        self.__board.render(self.__screen)
        self.__screen.move(curses.LINES-1, curses.COLS - 1)
        self.__screen.refresh()

    def play(self):
        dt = time.time()
        self.last_drop = time.time()

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
