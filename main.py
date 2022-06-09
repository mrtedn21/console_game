import curses
import time


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
        x = 1
        y = 1
        key = screen.getch()
        while key != 27:
            time.sleep(1 / 60)
            key = screen.getch()
            if key == 259:
                y -= 1
                x += 1
            if key == 258:
                y += 1
                x += 1
            screen.addstr(y, x, 'x')


if __name__ == '__main__':
    main()

