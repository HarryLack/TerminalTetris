import curses
import sys
import time

from components.board import Board
from components.border import Border
from components.piece import Piece, Tetronimo
from constants import BORDER_WIDTH, MIN_TICK_TIME, SCALE, TARGET_FRAME_TIME, TARGET_TICK_TIME
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
        self.__tick_rate = TARGET_TICK_TIME

        self.__logger.log(f"{GameController.__name__} init")

    def piece(self):
        pass

    def tick(self):
        pass

    def action(self):
        key = self.__screen.getch()
        # TODO: Vim keys?
        match key:
            case Key.w.value:
                # self.__logger.log("w")
                self.__board.drop()
                self.last_drop = time.time()
            case Key.s.value:
                # self.__logger.log("s")
                self.__board.down()
                self.last_drop = time.time()
            case Key.a.value:
                # self.__logger.log("a")
                self.__board.move_left()
            case Key.d.value:
                # self.__logger.log("d")
                self.__board.move_right()
            case Key.q.value:
                # self.__logger.log("q")
                self.__board.rotate_left()
            case Key.e.value:
                # self.__logger.log("e")
                self.__board.rotate_right()
            # ESC
            case Key.ESC.value:
                # self.__logger.log("esc")
                curses.endwin()
                sys.exit()
            case -1:
                # No input case
                pass
            case _:
                self.__logger.log(f"Code:{key} | Key:{chr(key)}")

    def update(self):
        if not self.__board.active_piece:
            self.__board.add_piece(Piece(kind=Tetronimo.I, position=(1, 1)))

        now = time.time()
        if (now - self.last_drop) > self.__tick_rate:
            self.__board.down()
            self.last_drop = now
            self.__tick_rate = max(self.__tick_rate*0.975, MIN_TICK_TIME)
            self.__logger.log(self.__tick_rate)

    def draw(self):
        self.__border.render(self.__screen)
        self.__board.render(self.__screen)
        self.__screen.addstr(0, 0, f"{self.__tick_rate}")
        # pylint: disable-next=no-member
        self.__screen.move(curses.LINES-1, curses.COLS - 1)
        self.__screen.refresh()

    def play(self):
        prev = time.time()
        self.last_drop = time.time()

        game_frame = 0
        while True:
            # now = time.time()
            # if (now - prev) < TARGET_FRAME_TIME:
            #     time.sleep(TARGET_FRAME_TIME-(now-prev))
            #     continue

            game_frame += 1

            self.action()
            self.update()

            self.draw()

            # prev = now
            self.tick()
