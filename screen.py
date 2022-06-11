import curses


class ScreenAccess:
    _screen_obj = None

    def __new__(cls):
        if cls._screen_obj is None:
            cls._screen_obj = curses.initscr()
            cls._screen_obj.nodelay(True)
            curses.noecho()
            curses.cbreak()
            cls._screen_obj.keypad(True)

        return cls._screen_obj

    @classmethod
    def destroy(cls):
        curses.nocbreak()
        cls._screen_obj.keypad(False)
        curses.echo()
        curses.endwin()
