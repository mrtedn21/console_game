class Person:
    HERO = 0
    ENEMY = 1

    HERO_CHAR = 'X'

    def __init__(self, y, x, kind):
        self.y = y
        self.x = x
        self.kind = kind
