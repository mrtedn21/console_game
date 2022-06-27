from exceptions import GameOverError
from exceptions import GameWinError
from game import Game
from screen import ScreenAccess

if __name__ == '__main__':
    state = None
    ScreenAccess()
    game = Game()
    try:
        game.play()
    except KeyboardInterrupt:
        pass
    except GameOverError:
        state = 'lose'
    except GameWinError:
        state = 'win'
    finally:
        ScreenAccess.destroy()
        if state == 'lose':
            print('You lose, game over')
        elif state == 'win':
            print('You win! Congratulations!')
        else:
            print('Exit from game')
