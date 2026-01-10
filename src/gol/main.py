from gol.engine import GameOfLife


def main():
    game = GameOfLife(5, 5)
    game.toggle(1, 2)
    game.toggle(2, 2)
    game.toggle(3, 2)

    print(game.grid)
    game.step()
    print(game.grid)


if __name__ == "__main__":
    main()
