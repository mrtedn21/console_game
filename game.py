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

        self.person_x = self.left + 1
        self.person_y = self.bottom + 1


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

    def _move_person_right(self):
        if self.person_x < self.right - 1:
            self.person_x += 1

    def _move_person_left(self):
        if self.person_x > self.left + 1:
            self.person_x -= 1

    def _move_person_down(self):
        if self.person_y < self.top - 1:
            self.person_y += 1

    def _move_person_up(self):
        if self.person_y > self.bottom + 1:
            self.person_y -= 1

    def play(self):
        self._draw_field_borders()
        key = self.screen.getch()
        while key != ESCAPE_KEY:
            self.screen.addch(self.person_y, self.person_x, 'X')
            self.screen.refresh()
            time.sleep(1 / 60)
            key = self.screen.getch()
            if key < 0:
                continue

            if key == UP_KEY:
                self._move_person_up()
            if key == DOWN_KEY:
                self._move_person_down()
            if key == RIGHT_KEY:
                self._move_person_right()
            if key == LEFT_KEY:
                self._move_person_left()

    def __exit__(self, *exceptions):
        close_screen(self.screen)

