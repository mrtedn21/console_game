from typing import Optional
import random

from game_field import GameField
from gameplay_utils import Cell
from gameplay_exceptions import GameOverError
from gameplay_utils import LittleFigureDetector, return_changes
from constants import MotionDirection, PositionChange


class GamePlay:
    def __init__(self, max_height: int, max_width: int):
        self._bottom = 0  # Bottom of game field
        self._top = max_height - 1  # Top of game field
        self._left = 0  # Left point of game field
        self._right = max_width - 1  # Right point of game field

        # Hero
        self._hero_y: int = 0
        self._hero_x: int = 0

        # Enemy
        self._enemy_y: int = 0
        self._enemy_x: int = 0
        self._enemy_steps_count: int = 0
        self._enemy_motion_direction: Optional[MotionDirection] = None

        self._game_field: GameField = GameField(max_height, max_width)

    @return_changes
    def init_borders_on_game_field(self):
        for i in range(self._top + 1):
            self._game_field.update_cell(
                PositionChange(new_y=i, new_x=0, value=Cell.BORDER)
            )
            self._game_field.update_cell(
                PositionChange(new_y=i, new_x=self._right, value=Cell.BORDER)
            )

        for j in range(self._right + 1):
            self._game_field.update_cell(
                PositionChange(new_y=0, new_x=j, value=Cell.BORDER)
            )
            self._game_field.update_cell(
                PositionChange(new_y=self._top, new_x=j, value=Cell.BORDER)
            )

    @return_changes
    def init_enemy_and_hero_on_game_field(self):
        self._hero_y = self._bottom + 1
        self._hero_x = self._left + 1
        self._game_field.update_cell(
            PositionChange(new_y=self._hero_y, new_x=self._hero_x, value=Cell.TRACK)
        )

        self._enemy_y = int((self._top - self._bottom) / 2)
        self._enemy_x = int((self._right - self._left) / 2)
        self._game_field.update_cell(
            PositionChange(new_y=self._enemy_y, new_x=self._enemy_x, value=Cell.ENEMY)
        )

    @return_changes
    def make_progress(self, hero_motion_direction: MotionDirection):
        self._move_hero(hero_motion_direction)
        self._move_enemy()

    def _move_hero(self, motion_direction: MotionDirection):
        if motion_direction == motion_direction.DO_NOTHING:
            return

        new_hero_y, new_hero_x = self._get_new_coordinates_by_motion_direction(
            self._hero_y,
            self._hero_x,
            motion_direction,
        )

        if self._is_border_reached(new_hero_y, new_hero_x):
            LittleFigureDetector(self._game_field).detect()

        if not self._can_person_go(new_hero_y, new_hero_x):
            return

        self._hero_y = new_hero_y
        self._hero_x = new_hero_x
        self._game_field.update_cell(
            PositionChange(new_y=new_hero_y, new_x=new_hero_x, value=Cell.TRACK)
        )

    def _move_enemy(self):
        if self._enemy_steps_count < 1:
            self._set_new_enemy_direction()

        new_enemy_y, new_enemy_x = self._get_new_coordinates_by_motion_direction(
            self._enemy_y,
            self._enemy_x,
            self._enemy_motion_direction,
        )

        if self._is_person_on_track(new_enemy_y, new_enemy_x):
            raise GameOverError

        if not self._can_person_go(new_enemy_y, new_enemy_x):
            self._set_new_enemy_direction()
            return

        self._game_field.update_cell(
            PositionChange(new_y=self._enemy_y, new_x=self._enemy_x, value=Cell.EMPTY)
        )
        self._game_field.update_cell(
            PositionChange(new_y=new_enemy_y, new_x=new_enemy_x, value=Cell.ENEMY)
        )

        self._enemy_y = new_enemy_y
        self._enemy_x = new_enemy_x
        self._enemy_steps_count -= 1

    def _set_new_enemy_direction(self):
        self._enemy_steps_count = self._get_new_steps_count(self._top)
        self._enemy_motion_direction = self._get_new_movement_direction(
            self._enemy_motion_direction,
        )

    def _can_person_go(
        self,
        new_y: int,
        new_x: int,
    ) -> bool:
        if self._game_field.get(new_y, new_x) == Cell.EMPTY:
            return True
        return False

    def _is_person_on_track(self, new_y: int, new_x: int) -> bool:
        try:
            if self._game_field.get(new_y, new_x) == Cell.TRACK:
                return True
            return False
        except IndexError:
            pass

    def _is_border_reached(self, new_y: int, new_x: int) -> bool:
        return self._game_field.get(new_y, new_x) in (Cell.BORDER, Cell.MARKED)

    def _is_on_track(self, new_y: int, new_x: int) -> bool:
        return self._game_field.get(new_y, new_x) == Cell.TRACK

    def _get_new_coordinates_by_motion_direction(
        self,
        old_y: int,
        old_x: int,
        motion_direction: MotionDirection,
    ) -> tuple[int, int]:
        decision_mapping = {
            MotionDirection.UP: lambda y, x: (y - 1, x),
            MotionDirection.DOWN: lambda y, x: (y + 1, x),
            MotionDirection.RIGHT: lambda y, x: (y, x + 1),
            MotionDirection.LEFT: lambda y, x: (y, x - 1),
        }

        return decision_mapping[motion_direction](old_y, old_x)

    def _get_new_steps_count(self, top: int) -> int:
        return random.randint(2, top)

    def _get_new_movement_direction(self, old_direction):
        new_dir = random.randint(1, 4)
        if new_dir == old_direction:
            return MotionDirection(self._get_new_movement_direction(new_dir))
        else:
            return MotionDirection(new_dir)
