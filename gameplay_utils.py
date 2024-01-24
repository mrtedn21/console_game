from enum import Enum
from typing import Optional
import random


class MotionDirection(Enum):
    UP = 1
    DOWN = 2
    RIGHT = 3
    LEFT = 4
    DO_NOTHING = 5


class Cell(Enum):
    """ This class presents cell on game field.
    Empty cell means usual cell. In start of
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
    BORDER = 1
    TRACK = 2
    CONSIDER = 3
    MARKED = 4
    ENEMY = 5


class GameField:
    def __init__(self, height: int, width: int):
        self._matrix: list[list[Cell]] = []
        self._changes: list[tuple] = []

        for i in range(height):
            self._matrix.append([])

            for j in range(width):
                self._matrix[i].append(Cell.EMPTY)

    def clear_changes(self):
        self._changes = []

    def get_changes(self):
        return self._changes

    def set(self, y: int, x: int, value: Cell):
        try:
            self._matrix[y][x] = value
            self._changes.append((y, x, value))
        except IndexError:
            pass

    def get(self, y: int, x: int) -> Optional[Cell]:
        try:
            return self._matrix[y][x]
        except IndexError:
            return None


# Helping functions


def _is_motion_horizontal(motion_direction: MotionDirection) -> bool:
    return motion_direction in (
        MotionDirection.RIGHT, MotionDirection.LEFT,
    )


def _can_person_go(
    game_field: GameField,
    new_y: int,
    new_x: int,
) -> bool:
    if game_field.get(new_y, new_x) == Cell.EMPTY:
        return True
    return False


def _is_person_on_track(game_field: GameField, new_y: int, new_x: int) -> bool:
    try:
        if game_field.get(new_y, new_x) == Cell.TRACK:
            return True
        return False
    except IndexError:
        pass


def _is_border_reached(game_field: GameField, new_y: int, new_x: int) -> bool:
    return game_field.get(new_y, new_x) in (Cell.BORDER, Cell.MARKED)


def _is_on_track(game_field: GameField, new_y: int, new_x: int) -> bool:
    return game_field.get(new_y, new_x) == Cell.TRACK


def _get_new_coordinates_by_motion_direction(
    old_y: int, old_x: int, motion_direction: MotionDirection,
) -> tuple[int, int]:
    decision_mapping = {
        MotionDirection.UP: lambda y, x: (y - 1, x),
        MotionDirection.DOWN: lambda y, x: (y + 1, x),
        MotionDirection.RIGHT: lambda y, x: (y, x + 1),
        MotionDirection.LEFT: lambda y, x: (y, x - 1),
    }

    return decision_mapping[motion_direction](old_y, old_x)


def _get_new_steps_count(top: int) -> int:
    return random.randint(2, top)


def _get_new_movement_direction(old_direction):
    new_dir = random.randint(1, 4)
    if new_dir == old_direction:
        return MotionDirection(_get_new_movement_direction(new_dir))
    else:
        return MotionDirection(new_dir)


def return_changes(func):
    def foo(self, *args, **kwargs):
        self._game_field.clear_changes()
        func(self, *args, **kwargs)
        return self._game_field.get_changes()
    return foo


class LittleFigureDetector:
    """ When hero reach border, whole game field became
    separated by two figures, the class needs to detect which
    of these figures is less, and then the class marked it"""

    def __init__(
        self,
        top: int,
        bottom: int,
        left: int,
        right: int,
        game_field: GameField,
    ):
        # ИЗБАВИТЬСЯ ОТ ТОПОВ И ЛЕФТОВ ТУТ, ОНИ ИЗЛИШНИ!
        self._top = top
        self._bottom = bottom
        self._left = left
        self._right = right
        self._game_field = game_field

    def detect(self):
        self._fill_one_figure()
        self._select_little_figure()

    def _select_little_figure(self):
        empty_count = 0
        considered_count = 0
        for i in self._game_field._matrix:
            for j in i:
                if j == Cell.EMPTY:
                    empty_count += 1
                if j == Cell.CONSIDER:
                    considered_count += 1

        for y in range(self._top):
            for x in range(self._right):
                if empty_count < considered_count:
                    if self._game_field.get(y, x) == Cell.EMPTY:
                        self._game_field.set(y, x, Cell.MARKED)
                    if self._game_field.get(y, x) == Cell.CONSIDER:
                        self._game_field.set(y, x, Cell.EMPTY)
                else:
                    if self._game_field.get(y, x) == Cell.CONSIDER:
                        self._game_field.set(y, x, Cell.MARKED)
                if self._game_field.get(y, x) == Cell.TRACK:
                    self._game_field.set(y, x, Cell.MARKED)

    def _fill_one_figure(self, y=None, x=None):
        if y is None or x is None:
            y, x = self._get_random_empty_coordinates()

        try:
            if self._game_field.get(y + 1, x) == Cell.EMPTY:
                self._game_field.set(y + 1, x, Cell.CONSIDER)
                self._fill_one_figure(y + 1, x)

            if self._game_field.get(y, x + 1) == Cell.EMPTY:
                self._game_field.set(y, x + 1, Cell.CONSIDER)
                self._fill_one_figure(y, x + 1)

            if self._game_field.get(y - 1, x) == Cell.EMPTY:
                self._game_field.set(y - 1, x, Cell.CONSIDER)
                self._fill_one_figure(y - 1, x)

            if self._game_field.get(y, x - 1) == Cell.EMPTY:
                self._game_field.set(y, x - 1, Cell.CONSIDER)
                self._fill_one_figure(y, x - 1)
        except IndexError:
            pass

    def _get_random_empty_coordinates(self):
        random.seed()
        y = random.randint(3, self._top - 2)
        x = random.randint(2, self._right - 2)
        if self._game_field.get(y, x) == Cell.EMPTY:
            return y, x
        return self._get_random_empty_coordinates()
