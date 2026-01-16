import numpy as np

from gol.engine import GameOfLife
from gol.ui.camera import Camera, screen_to_world, world_to_screen
from gol.config import (ALIVE_COLOR, CELL_SIZE, DEAD_COLOR, FPS, MAX_STEP,
                        MIN_STEP, POINT_COLOR, POINT_RADIUS, STEP_INTERVAL)

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


def test_world_to_screen_roundtrip():
    cell_size = CELL_SIZE
    cam = Camera(x=10, y=5, zoom=2)
    wx, wy = 12, 7
    sx, sy = world_to_screen(cam, wx, wy, cell_size)
    wx2, wy2 = screen_to_world(cam, sx, sy, cell_size)
    assert (wx, wy) == (int(wx2), int(wy2))
