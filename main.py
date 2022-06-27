from exceptions import GameOverError
from game import Game
from screen import ScreenAccess

if __name__ == '__main__':
    game_over = False
    ScreenAccess()
    game = Game()
    try:
        game.play()
    except KeyboardInterrupt:
        pass
    except GameOverError:
        game_over = True
    finally:
        ScreenAccess.destroy()
        if game_over:
            print('You lose, game over')
        else:
            print('Exit from game')
