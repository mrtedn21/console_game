import random
from constants import PositionChange
from constants import Cell

from game_field import GameField


def return_changes(func):
    def foo(self, *args, **kwargs):
        self._game_field.clear_changes()
        func(self, *args, **kwargs)
        return self._game_field.get_changes()

    return foo


class LittleFigureDetector:
    """When hero reach border, whole game field became
    separated by two figures, the class needs to detect which
    of these figures is less, and then the class marked it"""

    def __init__(self, game_field: GameField):
        self._game_field = game_field

    def detect(self):
        self._fill_one_figure()
        self._select_little_figure()

    def _select_little_figure(self):
        empty_count = 0
        considered_count = 0
        for i in self._game_field:
            if i == Cell.EMPTY:
                empty_count += 1
            if i == Cell.CONSIDER:
                considered_count += 1

        for y in range(self._game_field.height):
            for x in range(self._game_field.width):
                if empty_count < considered_count:
                    if self._game_field.get(y, x) == Cell.EMPTY:
                        self._game_field.update_cell(
                            PositionChange(new_y=y, new_x=x, value=Cell.MARKED)
                        )
                    if self._game_field.get(y, x) == Cell.CONSIDER:
                        self._game_field.update_cell(
                            PositionChange(new_y=y, new_x=x, value=Cell.EMPTY)
                        )
                else:
                    if self._game_field.get(y, x) == Cell.CONSIDER:
                        self._game_field.update_cell(
                            PositionChange(new_y=y, new_x=x, value=Cell.MARKED)
                        )
                if self._game_field.get(y, x) == Cell.TRACK:
                    self._game_field.update_cell(
                        PositionChange(new_y=y, new_x=x, value=Cell.MARKED)
                    )

    def _fill_one_figure(self, y=None, x=None):
        if y is None or x is None:
            y, x = self._get_random_empty_coordinates()

        try:
            if self._game_field.get(y + 1, x) == Cell.EMPTY:
                self._game_field.update_cell(
                    PositionChange(new_y=y + 1, new_x=x, value=Cell.CONSIDER)
                )
                self._fill_one_figure(y + 1, x)

            if self._game_field.get(y, x + 1) == Cell.EMPTY:
                self._game_field.update_cell(
                    PositionChange(new_y=y, new_x=x + 1, value=Cell.CONSIDER)
                )
                self._fill_one_figure(y, x + 1)

            if self._game_field.get(y - 1, x) == Cell.EMPTY:
                self._game_field.update_cell(
                    PositionChange(new_y=y - 1, new_x=x, value=Cell.CONSIDER)
                )
                self._fill_one_figure(y - 1, x)

            if self._game_field.get(y, x - 1) == Cell.EMPTY:
                self._game_field.update_cell(
                    PositionChange(new_y=y, new_x=x - 1, value=Cell.CONSIDER)
                )
                self._fill_one_figure(y, x - 1)
        except IndexError:
            pass

    def _get_random_empty_coordinates(self):
        random.seed()
        y = random.randint(3, self._game_field.height - 2)
        x = random.randint(2, self._game_field.width - 2)
        if self._game_field.get(y, x) == Cell.EMPTY:
            return y, x
        return self._get_random_empty_coordinates()
