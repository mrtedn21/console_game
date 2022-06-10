import curses


def get_screen():
    screen = curses.initscr()
    screen.nodelay(True)
    curses.noecho()
    curses.cbreak()
    screen.keypad(True)
    return screen


def close_screen(screen):
    curses.nocbreak()
    screen.keypad(False)
    curses.echo()
    curses.endwin()

