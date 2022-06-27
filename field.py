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
                if i in (self.bottom, self.top, 0):
                    self.matrix[i].append(Cell.BORDER)
                elif j in (self.right, self.left, 0):
                    self.matrix[i].append(Cell.BORDER)
                else:
                    self.matrix[i].append(Cell.EMPTY)

    def get_start_position(self, kind):
        if kind == Person.HERO:
            new_y = self.bottom + 1
            new_x = self.left + 1
            self.matrix[new_y][new_x] = Cell.TRACK

        elif kind == Person.ENEMY:
            new_y = int((self.top - self.bottom) / 2)
            new_x = int((self.right - self.left) / 2)

        else:
            raise TypeError('Unknown person kind')

        return new_y, new_x

    def _draw(self, *args, **kwargs):
        self.screen.addch(*args, **kwargs)

    def _is_border(self, y, x):
        return self.matrix[y][x] in (Cell.BORDER, Cell.MARKED)

    def _is_border_reach(self, person):
        return (
                person.x - person.px == 1 and self._is_border(person.y,
                                                              person.x + 1)
                or
                person.px - person.x == 1 and self._is_border(person.y,
                                                              person.x - 1)
                or
                person.y - person.py == 1 and self._is_border(person.y + 1,
                                                              person.x)
                or
                person.py - person.y == 1 and self._is_border(person.y - 1,
                                                              person.x)
        )

    def _move(self, person):
        if person.kind == Person.HERO:
            self.matrix[person.y][person.x] = Cell.TRACK
            self._draw(person.y, person.x, Person.HERO_CHAR)
            if self._is_border_reach(person):
                self.fill_one_figure()
                self.select_little_figure()
                self.draw_little_figure()
                self._draw(person.y, person.x, Person.HERO_CHAR)

        elif person.kind == Person.ENEMY:
            self._draw(person.y, person.x, Person.ENEMY_CHAR)
            self._draw(person.py, person.px, ' ')

        self.screen.refresh()

    def _is_empty(self, y, x):
        return self.matrix[y][x] == Cell.EMPTY

    def _is_on_track(self, person, y, x):
        try:
            if person.kind != Person.ENEMY:
                return False
            if self.matrix[y][x] == Cell.TRACK:
                return True
            return False
        except IndexError:
            pass

    def move_right(self, person):
        y, x = person.y, person.x

        if self._is_on_track(person, y, x + 1) \
                or self._is_on_track(person, y, x + 2):
            raise TypeError('You die!')

        if self._is_empty(y, x + 1):
            person.right()
            self._move(person)
        else:
            return

        if self._is_empty(y, x + 2):
            person.right()
            self._move(person)

    def move_left(self, person):
        y, x = person.y, person.x

        if self._is_on_track(person, y, x - 1) \
                or self._is_on_track(person, y, x - 2):
            raise TypeError('You die!')

        if self._is_empty(y, x - 1):
            person.left()
            self._move(person)
        else:
            return

        if self._is_empty(y, x - 2):
            person.left()
            self._move(person)

    def move_down(self, person):
        y, x = person.y, person.x

        if self._is_on_track(person, y + 1, x):
            raise TypeError('You die!')

        if self._is_empty(y + 1, x):
            person.down()
            self._move(person)

    def move_up(self, person):
        y, x = person.y, person.x

        if self._is_on_track(person, y - 1, x):
            raise TypeError('You die!')

        if self._is_empty(y - 1, x):
            person.up()
            self._move(person)

    def select_little_figure(self):
        empty_count = 0
        considered_count = 0
        for i in self.matrix:
            for j in i:
                if j == Cell.EMPTY:
                    empty_count += 1
                if j == Cell.CONSIDER:
                    considered_count += 1

        for y in range(self.top):
            for x in range(self.right):
                if empty_count < considered_count:
                    if self.matrix[y][x] == Cell.EMPTY:
                        self.matrix[y][x] = Cell.MARKED
                    if self.matrix[y][x] == Cell.CONSIDER:
                        self.matrix[y][x] = Cell.EMPTY
                else:
                    if self.matrix[y][x] == Cell.CONSIDER:
                        self.matrix[y][x] = Cell.MARKED
                if self.matrix[y][x] == Cell.TRACK:
                    self.matrix[y][x] = Cell.MARKED

    def draw_little_figure(self):
        for y in range(self.top):
            for x in range(self.right):
                if self.matrix[y][x] == Cell.MARKED:
                    self._draw(y, x, Person.HERO_CHAR)

        self.screen.refresh()

    def fill_one_figure(self, y=None, x=None):
        if y is None or x is None:
            y, x = self._get_random_empty_coordinates()

        try:
            if self.matrix[y + 1][x] == Cell.EMPTY:
                self.matrix[y + 1][x] = Cell.CONSIDER
                self.fill_one_figure(y + 1, x)

            if self.matrix[y][x + 1] == Cell.EMPTY:
                self.matrix[y][x + 1] = Cell.CONSIDER
                self.fill_one_figure(y, x + 1)

            if self.matrix[y - 1][x] == Cell.EMPTY:
                self.matrix[y - 1][x] = Cell.CONSIDER
                self.fill_one_figure(y - 1, x)

            if self.matrix[y][x - 1] == Cell.EMPTY:
                self.matrix[y][x - 1] = Cell.CONSIDER
                self.fill_one_figure(y, x - 1)
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
