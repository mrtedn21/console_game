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
        self.matrix = []
        self._fill_matrix()

    def _fill_matrix(self):
        for i in range(self.top):
            self.matrix.append([])
            for j in range(self.right):
                self.matrix[i].append(Cell.EMPTY)

    def get_start_position(self, kind):
        if kind == Person.HERO:
            new_y = self.bottom + 1
            new_x = self.left + 1

            self.matrix[new_y][new_x] = Cell.TRACK
            return new_y, new_x

    def _draw(self, *args, **kwargs):
        self.screen.addch(*args, **kwargs)

    def _is_on_border(self, y, x):
        return y in (self.top - 1, self.bottom + 1) \
            or x in (self.right - 1, self.left + 1)

    def draw_person(self, person):
        if person.kind == Person.HERO:
            self.matrix[person.y][person.x] = Cell.TRACK

            self._draw(person.y, person.x, Person.HERO_CHAR)

            if self._is_on_border(person.y, person.x) \
                    and self._is_on_border(person.py, person.px):
                self._draw(person.py, person.px, ' ')

    def move_right(self, person):
        if person.x < self.right - 2:
            person.right()
            self.draw_person(person)
            person.right()
        elif person.x < self.right - 1:
            person.right()

        self.draw_person(person)

    def move_left(self, person):
        if person.x > self.left + 2:
            person.left()
            self.draw_person(person)
            person.left()
        elif person.x > self.left + 1:
            person.left()

        self.draw_person(person)

    def move_down(self, person):
        if person.y < self.top - 1:
            person.down()
            self.draw_person(person)

    def move_up(self, person):
        if person.y > self.bottom + 1:
            person.up()
            self.draw_person(person)

    def draw_borders(self):
        vertical_line = '│'
        horizontal_line = '─'

        for current in range(self.left, self.right):
            self._draw(self.bottom, current, horizontal_line)
            self._draw(self.top, current, horizontal_line)

        for current in range(self.bottom, self.top):
            self._draw(current, self.left, vertical_line)
            self._draw(current, self.right, vertical_line)

        self._draw(self.top, self.left, '└')
        self._draw(self.top, self.right, '┘')
        self._draw(self.bottom, self.left, '┌')
        self._draw(self.bottom, self.right, '┐')
