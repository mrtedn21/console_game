import curses
import time
from datetime import datetime


class Screen:
    def __enter__(self):
        self.screen = curses.initscr()
        self.screen.nodelay(True)
        curses.noecho()
        curses.cbreak()
        self.screen.keypad(True)
        return self.screen

    def __exit__(self, *exceptions):
        curses.nocbreak()
        self.screen.keypad(False)
        curses.echo()
        curses.endwin()

def main():
    with Screen() as screen:
        res = []
        initial_time = datetime.now()
        x = 1
        y = 1

        key = screen.getch()
        while key != 27:
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

        print(res)


if __name__ == '__main__':
    main()

