import curses
import time

from screen import get_screen
from screen import close_screen

ESCAPE_KEY = 27
UP_KEY = 259
DOWN_KEY = 258
LEFT_KEY = 260
RIGHT_KEY = 261

class Game:
    def __init__(self):
        self.screen = get_screen()
        
        self.bottom = 1
        self.top = curses.LINES - 2
        self.left = 1
        self.right = curses.COLS - 1

    def __enter__(self):
        return self

    def _draw_field_borders(self):
        vertical_line = '│'
        horizonatl_line = '─'

        for current in range(self.left, self.right):
            self.screen.addch(self.bottom, current, horizonatl_line)
            self.screen.addch(self.top, current, horizonatl_line)

        for current in range(self.bottom, self.top):
            self.screen.addch(current, self.left, vertical_line)
            self.screen.addch(current, self.right, vertical_line)

        self.screen.addch(self.top, self.left, '└')
        self.screen.addch(self.top, self.right, '┘')
        self.screen.addch(self.bottom, self.left, '┌')
        self.screen.addch(self.bottom, self.right, '┐')

        self.screen.refresh()

    def play(self):
        self._draw_field_borders()
        x = self.left + 1
        y = self.bottom + 1
        key = self.screen.getch()
        while key != ESCAPE_KEY:
            self.screen.addch(y, x, 'X')
            self.screen.refresh()
            time.sleep(1 / 60)
            key = self.screen.getch()
            if key < 0:
                continue

            if key == UP_KEY:
                y -= 1
            if key == DOWN_KEY:
                y += 1
            if key == RIGHT_KEY:
                x += 1
            if key == LEFT_KEY:
                x -= 1

    def __exit__(self, *exceptions):
        close_screen(self.screen)

