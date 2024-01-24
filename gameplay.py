from typing import Optional

from game_field import Cell, GameField
from gameplay_exceptions import GameOverError
from gameplay_utils import (
    LittleFigureDetector,
    MotionDirection,
    _can_person_go,
    _get_new_coordinates_by_motion_direction,
    _get_new_movement_direction,
    _get_new_steps_count,
    _is_border_reached,
    _is_motion_horizontal,
    _is_person_on_track,
    return_changes
)


class GamePlay:
    def __init__(self, max_height: int, max_width: int):
        self._bottom = 0  # Bottom of game field
        self._top = max_height - 1  # Top of game field
        self._left = 0  # Left point of game field
        self._right = max_width - 1  # Right point of game field
        self._game_field = GameField(self._top + 1, self._right + 1)

        # Hero
        self._hero_y: int = 0
        self._hero_x: int = 0

        # Enemy
        self._enemy_y: int = 0
        self._enemy_x: int = 0
        self._enemy_steps_count: int = 0
        self._enemy_motion_direction: Optional[MotionDirection] = None

    @return_changes
    def init_borders_on_game_field(self):
        for i in range(self._top + 1):
            self._game_field.set(i, 0, Cell.BORDER)
            self._game_field.set(i, self._right, Cell.BORDER)

        for j in range(self._right + 1):
            self._game_field.set(0, j, Cell.BORDER)
            self._game_field.set(self._top, j, Cell.BORDER)

    @return_changes
    def init_enemy_and_hero_on_game_field(self):
        self._hero_y = self._bottom + 1
        self._hero_x = self._left + 1
        self._game_field.set(self._hero_y, self._hero_x, Cell.TRACK)

        self._enemy_y = int((self._top - self._bottom) / 2)
        self._enemy_x = int((self._right - self._left) / 2)
        self._game_field.set(self._enemy_y, self._enemy_x, Cell.ENEMY)

    @return_changes
    def make_progress(self, hero_motion_direction: MotionDirection):
        self._move_hero(hero_motion_direction)
        self._move_enemy()

    def _move_hero(
        self,
        motion_direction: MotionDirection,
        _need_another_motion: bool = True,
    ):
        """ _need_another_motion is argument for internal logic. If person
        goes to left or to right, this motion must be duplicated. Because
        on terminal, places for words are high and narrow, and one motion
        up or down visually equal to two motions to left or to right"""

        if motion_direction == motion_direction.DO_NOTHING:
            return

        new_hero_y, new_hero_x = _get_new_coordinates_by_motion_direction(
            self._hero_y, self._hero_x, motion_direction,
        )

        if _is_border_reached(self._game_field, new_hero_y, new_hero_x):
            detector = LittleFigureDetector(
                top=self._top, bottom=self._bottom,
                left=self._left, right=self._right,
                game_field=self._game_field,
            )
            detector.detect()

        if not _can_person_go(self._game_field, new_hero_y, new_hero_x):
            return

        self._hero_y = new_hero_y
        self._hero_x = new_hero_x
        self._game_field.set(new_hero_y, new_hero_x, Cell.TRACK)

        if _is_motion_horizontal(motion_direction) and _need_another_motion:
            self._move_hero(motion_direction, False)

    def _move_enemy(self, _need_another_motion: bool = True):
        if self._enemy_steps_count < 1:
            self._enemy_steps_count = _get_new_steps_count(self._top)
            self._enemy_motion_direction = _get_new_movement_direction(
                self._enemy_motion_direction,
            )

        new_enemy_y, new_enemy_x = _get_new_coordinates_by_motion_direction(
            self._enemy_y, self._enemy_x, self._enemy_motion_direction,
        )

        if _is_person_on_track(self._game_field, new_enemy_y, new_enemy_x):
            raise GameOverError

        if _is_motion_horizontal(self._enemy_motion_direction):
            self._enemy_steps_count -= 1
        else:
            self._enemy_steps_count -= 2

        if not _can_person_go(self._game_field, new_enemy_y, new_enemy_x):
            return

        self._game_field.set(self._enemy_y, self._enemy_x, Cell.EMPTY)
        self._game_field.set(new_enemy_y, new_enemy_x, Cell.ENEMY)

        self._enemy_y = new_enemy_y
        self._enemy_x = new_enemy_x

        if all((
            _is_motion_horizontal(self._enemy_motion_direction),
            _need_another_motion,
        )):
            self._move_enemy(False)
        else:
            self._enemy_steps_count -= 1
