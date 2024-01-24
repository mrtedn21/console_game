from enum import Enum
from typing import Optional


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
