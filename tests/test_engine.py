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


def test_undo_restores_previous_state():
    game = GameOfLife(5, 5)

    game.toggle(2, 1)
    game.toggle(2, 2)
    game.toggle(2, 3)

    before = game.grid.copy()
    game.step()
    game.undo()

    assert np.array_equal(game.grid, before)


def test_toggle_can_be_undone():
    game = GameOfLife(5, 5)

    game.toggle(2, 2)
    assert game.grid[2, 2] == 1

    game.undo()
    assert game.grid[2, 2] == 0
