import sys
import asyncio
import time
from collections import defaultdict

from gameplay import GamePlay
from gameplay_exceptions import GameOverError, GameWinError
from constants import MotionDirection
from terminal import Terminal


ESCAPE_KEY = 27
UP_KEY = 259
DOWN_KEY = 258
LEFT_KEY = 260
RIGHT_KEY = 261


pressed_key_to_motion_direction = defaultdict(
    lambda: MotionDirection.DO_NOTHING,
    {
        UP_KEY: MotionDirection.UP,
        DOWN_KEY: MotionDirection.DOWN,
        LEFT_KEY: MotionDirection.LEFT,
        RIGHT_KEY: MotionDirection.RIGHT,
    },
)


async def move_hero(terminal, game_play):
    pressed_key = terminal.get_pressed_key()
    while pressed_key != ESCAPE_KEY:
        motion_direction = pressed_key_to_motion_direction[pressed_key]

        changes = game_play.move_hero(motion_direction)
        terminal.print_changes(changes)
        await asyncio.sleep(1 / 100)

        pressed_key = terminal.get_pressed_key()


async def move_enemy(terminal, game_play):
    while True:
        changes = game_play.move_enemy()
        terminal.print_changes(changes)
        await asyncio.sleep(1 / 20)


async def main():
    terminal = Terminal()
    max_y, max_x = terminal.get_max_y_and_x()
    sys.setrecursionlimit(max_y * max_x * 2)

    game_play = GamePlay(max_y, max_x)

    changes = game_play.init_borders_on_game_field()
    terminal.print_changes(changes)

    changes = game_play.init_enemy_and_hero_on_game_field()
    terminal.print_changes(changes)

    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(move_enemy(terminal, game_play))
            tg.create_task(move_hero(terminal, game_play))

    except KeyboardInterrupt:
        terminal.destroy("Exit from game")
    except GameOverError:
        terminal.destroy("You lose, game over")
    except GameWinError:
        terminal.destroy("You win! Congratulations!")
    finally:
        terminal.destroy()


if __name__ == "__main__":
    asyncio.run(main())
