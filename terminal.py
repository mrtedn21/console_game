import curses

from gameplay_utils import Cell


cell_type_to_terminal_char = {
    Cell.EMPTY: ' ',
    Cell.BORDER: '█',
    Cell.TRACK: 'X',
    Cell.CONSIDER: ' ',
    Cell.MARKED: 'X',
    Cell.ENEMY: 'O',
}


class Terminal:
    def __init__(self):
        self._screen_obj = curses.initscr()
        self._screen_obj.nodelay(True)
        curses.noecho()
        curses.cbreak()
        self._screen_obj.keypad(True)

    def get_max_y_and_x(self):
        return self._screen_obj.getmaxyx()

    def get_pressed_key(self):
        return self._screen_obj.getch()

    def destroy(self, print_text_after_destroy: str = ''):
        curses.nocbreak()
        self._screen_obj.keypad(False)
        curses.echo()
        curses.endwin()

        if print_text_after_destroy:
            print(print_text_after_destroy)

    def print_changes(self, changes: list):
        for y, x, cell_type in changes:
            char = cell_type_to_terminal_char[cell_type]
            try:
                self._screen_obj.addch(y, x, char)
            except curses.error:
                pass

        self._screen_obj.refresh()
