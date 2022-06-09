import curses


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
