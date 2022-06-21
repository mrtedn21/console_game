import sys
import time

from field import Field
from person import Person
from screen import ScreenAccess

ESCAPE_KEY = 27
UP_KEY = 259
DOWN_KEY = 258
LEFT_KEY = 260
RIGHT_KEY = 261


class Game:
    def __init__(self):
        max_y, max_x = ScreenAccess().getmaxyx()
        sys.setrecursionlimit(max_x * max_y)
        self.field = Field(
            max_width=max_x,
            max_height=max_y,
        )
        self.hero = Person(
            *self.field.get_start_position(Person.HERO),
            Person.HERO
        )

    def play(self):
        screen = ScreenAccess()
        self.field.draw_borders()

        key = screen.getch()
        while key != ESCAPE_KEY:
            time.sleep(1 / 60)
            key = screen.getch()
            if key < 0:
                continue

            if key == UP_KEY:
                self.field.move_up(self.hero)
            if key == DOWN_KEY:
                self.field.move_down(self.hero)
            if key == RIGHT_KEY:
                self.field.move_right(self.hero)
            if key == LEFT_KEY:
                self.field.move_left(self.hero)
