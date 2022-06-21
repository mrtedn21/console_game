from game import Game
from screen import ScreenAccess

if __name__ == '__main__':
    ScreenAccess()
    game = Game()
    try:
        game.play()
    except KeyboardInterrupt:
        pass
    finally:
        ScreenAccess.destroy()
        print('Exit from game')
