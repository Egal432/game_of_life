from gol.engine import GameOfLife

def test_block_is_stable():
    game = GameOfLife(4, 4)

    # 2x2 block
    game.toggle(1, 1)
    game.toggle(1, 2)
    game.toggle(2, 1)
    game.toggle(2, 2)

    before = [row[:] for row in game.grid]
    game.step()

    assert game.grid == before

