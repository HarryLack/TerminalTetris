
import curses

from constants import HEIGHT, TARGET_FRAME_TIME, WIDTH
from errors import ScreenSizeException
from logger import Logger
from game_controller import GameController


def main(stdscr: curses.window):
    logger = Logger()
    logger.log("Hello, World!")
    logger.log(f"Target Frame Rate:{TARGET_FRAME_TIME}")

    game = GameController(screen=stdscr, width=WIDTH, height=HEIGHT)

    game.play()


if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except curses.error as err:
        print(f"{err}")
    except ScreenSizeException as err:
        print(f"{err}")
