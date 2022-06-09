import curses
import time
from datetime import datetime


def main():
    screen = curses.initscr()
    screen.nodelay(True)
    curses.noecho()
    curses.cbreak()
    screen.keypad(True)
    res = []
    initial_time = datetime.now()
    x = 1
    y = 1

    while True:
        key = screen.getch()
        if key > 0:
            res.append(key)
        if key == 259:
            x += 1
            y -= 1
        if key == 258:
            x += 1
            y += 1
        screen.addstr(y, x, 'x')
        if (datetime.now() - initial_time).total_seconds() > 10:
            break

    curses.nocbreak()
    screen.keypad(False)
    curses.echo()
    curses.endwin()
    print(res)


if __name__ == '__main__':
    main()
    #try:
    #    main()
    #except BaseException as e:
    #    raise e
    #finally:
    #    curses.endwin()

