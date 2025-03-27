
import os


def create_world(width, height):
    world = ""
    for i in range(height):
        for j in range(width):
            if i == 0 or i == height-1:
                world += "#"
            else:
                if j == 0 or j == width-1:
                    world += "#"
                else:
                    world += " "
        world += "\n"
    return world


def clear_console(stdscr):
    stdscr.clear()
