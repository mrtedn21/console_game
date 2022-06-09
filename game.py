import curses
import time

from screen import Screen

ESCAPE_KEY = 27
UP_KEY = 259
DOWN_KEY = 258
LEFT_KEY = 260
RIGHT_KEY = 261


class Game:
    def __init__(self):
        pass

    def play(self):
        with Screen() as screen:
            x = 0
            y = 0
            key = screen.getch()
            while key != ESCAPE_KEY:
                screen.addch(y, x, 'X')
                screen.refresh()
                time.sleep(1 / 60)
                key = screen.getch()
                if key < 0:
                    continue

                if key == UP_KEY:
                    y -= 1
                if key == DOWN_KEY:
                    y += 1
                if key == RIGHT_KEY:
                    x += 1
                if key == LEFT_KEY:
                    x -= 1
