
import curses
import sys
import time

from render import clear_console, create_world
from game import I_STATES, Board, Piece, Orientation


WIDTH = 12
HEIGHT = 22
SCALE = 1
TARGET_FRAME_RATE = 30
# ms per frameas seconds
TARGET_FRAME_TIME = (1000.0/TARGET_FRAME_RATE)/1000


def log(thing):
    print(thing, end="")


def main(stdscr: curses.window):
    log(TARGET_FRAME_TIME)
    log("Hello, World!")

    dt = time.time()

    iter = 0

    while (True and iter < 1000):
        # TODO Make this actually game loop
        key = stdscr.getch()
        log(f"Key:{key}")
        match key:
            # s
            case 115:
                log("s")
            # a
            case 97:
                log("a")
            # d
            case 100:
                log("d")
            # q
            case 113:
                log("q")
            # ESC
            case 27:
                log("esc")
                curses.endwin()
                return

        iter += 1
        now = time.time()
        if (now - dt) < TARGET_FRAME_TIME:
            time.sleep(TARGET_FRAME_TIME-(now-dt))
            continue

        # key = sys.stdin.read(1)
        # log("key:", key)

        stdscr.addstr(0, 0, create_world(WIDTH, HEIGHT))
        stdscr.addstr(f"{iter}")
        offset = 3
        for (y, x) in I_STATES[Orientation.NONE]:
            stdscr.addch(y+offset, x+offset, "@")

        dt = now
        stdscr.move(curses.LINES-1, curses.COLS - 1)
        stdscr.refresh()


curses.wrapper(main)
