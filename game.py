import time

from screen import Screen


class Game:
    def __init__(self):
        pass

    def play(self):
        with Screen() as screen:
            x = 1
            y = 1
            key = screen.getch()
            while key != 27:
                time.sleep(1 / 60)
                key = screen.getch()
                if key == 259:
                    y -= 1
                    x += 1
                if key == 258:
                    y += 1
                    x += 1
                screen.addstr(y, x, 'x')
