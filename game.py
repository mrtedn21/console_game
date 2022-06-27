import random
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
        self.enemy = Person(
            *self.field.get_start_position(Person.ENEMY),
            Person.ENEMY
        )

    def play(self):
        screen = ScreenAccess()
        self.field.draw_borders()

        key = screen.getch()
        while key != ESCAPE_KEY:
            # Enemy logic
            if not self.enemy.steps_count:
                self.enemy.steps_count = random.randint(2, self.field.top)
                self.enemy.direction = get_new_direction(
                    self.enemy.direction
                )

            if self.enemy.direction == 0:
                self.field.move_up(self.enemy)
            if self.enemy.direction == 1:
                self.field.move_down(self.enemy)
            if self.enemy.direction == 2:
                self.field.move_left(self.enemy)
            if self.enemy.direction == 3:
                self.field.move_right(self.enemy)

            self.enemy.steps_count -= 1

            # game logic
            time.sleep(1 / 20)
            key = screen.getch()
            if key < 0:
                continue

            # Hero logic
            if key == UP_KEY:
                self.field.move_up(self.hero)
            if key == DOWN_KEY:
                self.field.move_down(self.hero)
            if key == RIGHT_KEY:
                self.field.move_right(self.hero)
            if key == LEFT_KEY:
                self.field.move_left(self.hero)


def get_new_direction(old_direction):
    new_dir = random.randint(0, 3)
    if new_dir == old_direction:
        return get_new_direction(new_dir)
    else:
        return new_dir
