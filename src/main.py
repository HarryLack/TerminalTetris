
import curses
import sys
import time

from constants import HEIGHT, TARGET_FRAME_TIME, WIDTH
from logger import Logger
from render import clear_console, create_world
from game import I_STATES, Board, GameController, Piece, Orientation


def main(stdscr: curses.window):
    logger = Logger()
    logger.log("Hello, World!")
    logger.log(f"Target Frame Rate:{TARGET_FRAME_TIME}")

    game = GameController(screen=stdscr, width=WIDTH, height=HEIGHT)

    game.play()


if __name__ == "__main__":
    curses.wrapper(main)
