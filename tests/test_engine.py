import numpy as np
from gol.engine import GameOfLife

def test_block_is_stable():
    game = GameOfLife(4, 4)

    # 2x2 block
    game.toggle(1, 1)
    game.toggle(1, 2)
    game.toggle(2, 1)
    game.toggle(2, 2)

    before = game.grid.copy()
    game.step()

    assert np.array_equal(game.grid, before)
