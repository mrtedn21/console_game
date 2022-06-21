import random
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

    EMPTY = ' '
    BORDER = 'B'
    TRACK = 'X'
    CONSIDER = 'c'
    MARKED = 'm'


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
        for i in range(self.top + 1):
            self.matrix.append([])
            for j in range(self.right + 1):
                if i in (self.bottom, self.top):
                    self.matrix[i].append(Cell.BORDER)
                elif j in (self.right, self.left):
                    self.matrix[i].append(Cell.BORDER)
                else:
                    self.matrix[i].append(Cell.EMPTY)

    def get_start_position(self, kind):
        if kind == Person.HERO:
            new_y = self.bottom + 1
            new_x = self.left + 1

            self.matrix[new_y][new_x] = Cell.TRACK
            return new_y, new_x

    def _draw(self, *args, **kwargs):
        self.screen.addch(*args, **kwargs)
        # TODO needs to remove refresh in _draw
        self.screen.refresh()

    def _is_on_border(self, y, x):
        return y in (self.top - 1, self.bottom + 1) \
            or x in (self.right - 1, self.left + 1)

    def _move(self, person):
        if person.kind == Person.HERO:
            self.matrix[person.y][person.x] = Cell.TRACK
            self._draw(person.y, person.x, Person.HERO_CHAR)

            if self._is_on_border(person.y, person.x):
                if self._is_on_border(person.py, person.px):
                    self._draw(person.py, person.px, ' ')

                if not self._is_on_border(person.py, person.px):
                    self.fill_little_empty_space()

    def move_right(self, person):
        if person.x < self.right - 2:
            person.right()
            self._move(person)
            person.right()

        elif person.x < self.right - 1:
            person.right()

        self._move(person)

    def move_left(self, person):
        if person.x > self.left + 2:
            person.left()
            self._move(person)
            person.left()

        elif person.x > self.left + 1:
            person.left()

        self._move(person)

    def move_down(self, person):
        if person.y < self.top - 1:
            person.down()
            self._move(person)

    def move_up(self, person):
        if person.y > self.bottom + 1:
            person.up()
            self._move(person)

    def fill_little_empty_space(self, y=None, x=None):
        if y is None or x is None:
            y, x = self._get_random_empty_coordinates()

        try:
            if self.matrix[y + 1][x] == Cell.EMPTY:
                self.matrix[y + 1][x] = Cell.CONSIDER
                self._draw(y + 1, x, Cell.CONSIDER.value)
                self.fill_little_empty_space(y + 1, x)

            if self.matrix[y][x + 1] == Cell.EMPTY:
                self.matrix[y][x + 1] = Cell.CONSIDER
                self._draw(y, x + 1, Cell.CONSIDER.value)
                self.fill_little_empty_space(y, x + 1)

            if self.matrix[y - 1][x] == Cell.EMPTY:
                self.matrix[y - 1][x] = Cell.CONSIDER
                self._draw(y - 1, x, Cell.CONSIDER.value)
                self.fill_little_empty_space(y - 1, x)

            if self.matrix[y][x - 1] == Cell.EMPTY:
                self.matrix[y][x - 1] = Cell.CONSIDER
                self._draw(y, x - 1, Cell.CONSIDER.value)
                self.fill_little_empty_space(y, x - 1)
        except IndexError:
            pass

    def _get_random_empty_coordinates(self):
        random.seed()
        y = random.randint(3, self.top - 2)
        x = random.randint(2, self.right - 2)
        if self.matrix[y][x] == Cell.EMPTY:
            return y, x
        return self._get_random_empty_coordinates()

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

        self.screen.refresh()
