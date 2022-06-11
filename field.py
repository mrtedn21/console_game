from enum import Enum

from person import Person
from screen import ScreenAccess


class Cell(Enum):
    """ This class presents cell on game field
    empty cell means usual cell. In start of
    game all cells are empty. Track cell means
    temp marked. Cell become track when game
    person move, behind him remains track of
    marked cells. But if enemy will cross over
    the track, game person lose and die, and
    track cells became again empty. Last type
    is marked, cell becomes marked when person
    successfully moves from one border to anoter
    and all shape that drawed by track becomes
    marked, forever """

    EMPTY = 0
    TRACK = 1
    MARKED = 2

    LEFT = 3
    RIGHT = 4


class Field:
    def __init__(self, max_width, max_height):
        self.bottom = 1
        self.top = max_height - 2
        self.left = 1
        self.right = max_width - 1

        self.screen = ScreenAccess()

    def get_start_position(self, kind):
        if kind == Person.HERO:
            new_y = self.bottom + 1
            new_x = self.left + 1

            self.draw(new_y, new_x, Person.HERO_CHAR)
            return new_y, new_x

    def draw(self, *args, **kwargs):
        self.screen.addch(*args, **kwargs)

    def draw_person(self, person):
        self.draw(person.y, person.x, 'X')

    def move_right(self, person):
        if person.x < self.right - 2:
            person.x += 1
            self.draw_person(person)
            person.x += 1
        elif person.x < self.right - 1:
            person.x += 1

        self.draw_person(person)

    def move_left(self, person):
        if person.x > self.left + 2:
            person.x -= 1
            self.draw_person(person)
            person.x -= 1
        elif person.x > self.left + 1:
            person.x -= 1

        self.draw_person(person)

    def move_down(self, person):
        if person.y < self.top - 1:
            person.y += 1
            self.draw_person(person)

    def move_up(self, person):
        if person.y > self.bottom + 1:
            person.y -= 1
            self.draw_person(person)

    def draw_borders(self):
        vertical_line = '│'
        horizontal_line = '─'

        for current in range(self.left, self.right):
            self.draw(self.bottom, current, horizontal_line)
            self.draw(self.top, current, horizontal_line)

        for current in range(self.bottom, self.top):
            self.draw(current, self.left, vertical_line)
            self.draw(current, self.right, vertical_line)

        self.draw(self.top, self.left, '└')
        self.draw(self.top, self.right, '┘')
        self.draw(self.bottom, self.left, '┌')
        self.draw(self.bottom, self.right, '┐')
