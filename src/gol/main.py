from gol.engine import GameOfLife
from gol.ui.pygame_ui import run


def main():
    game = GameOfLife(80, 60)
    game.toggle(39, 30)
    game.toggle(40, 30)
    game.toggle(41, 30)
    game.toggle(42, 30)
    game.toggle(42, 32)
    game.toggle(42, 31)
    game.toggle(42, 33)
    game.toggle(43, 31)
    game.toggle(44, 31)
    run(game)


if __name__ == "__main__":
    main()
