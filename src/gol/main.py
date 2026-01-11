from gol.engine import GameOfLife
from gol.ui.pygame_ui import run


def main():
    game = GameOfLife(80, 60)
    game.toggle(39, 30)
    game.toggle(40, 30)
    game.toggle(41, 30)

    run(game)


if __name__ == "__main__":
    main()
