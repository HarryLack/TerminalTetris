
import curses

from constants import HEIGHT, TARGET_FRAME_TIME, WIDTH
from logger import Logger
from game import GameController


def main(stdscr: curses.window):
    logger = Logger()
    logger.log("Hello, World!")
    logger.log(f"Target Frame Rate:{TARGET_FRAME_TIME}")

    game = GameController(screen=stdscr, width=WIDTH, height=HEIGHT)

    game.play()


if __name__ == "__main__":
    curses.wrapper(main)
