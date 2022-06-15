class Person:
    HERO = 0
    ENEMY = 1

    HERO_CHAR = 'X'

    def __init__(self, y, x, kind):
        self.y = y
        self.x = x

        # px and py means previous x and y
        self.py = y
        self.px = x

        self.kind = kind

    def left(self):
        self.px = self.x
        self.py = self.y
        self.x -= 1

    def right(self):
        self.px = self.x
        self.py = self.y
        self.x += 1

    def up(self):
        self.py = self.y
        self.px = self.x
        self.y -= 1

    def down(self):
        self.py = self.y
        self.px = self.x
        self.y += 1
