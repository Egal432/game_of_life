import numpy as np


class GameOfLife:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = np.zeros((height, width), dtype=np.uint8)

    def clear(self) -> None:
        self.grid.fill(0)

    def toggle(self, x: int, y: int) -> None:
        self.grid[y, x] ^= 1

    def alive(self, x: int, y: int) -> bool:
        return bool(self.grid[y, x])

    def step(self) -> None:
        neighbors = (
            np.roll(self.grid, 1, 0)
            + np.roll(self.grid, -1, 0)
            + np.roll(self.grid, 1, 1)
            + np.roll(self.grid, -1, 1)
            + np.roll(np.roll(self.grid, 1, 0), 1, 1)
            + np.roll(np.roll(self.grid, 1, 0), -1, 1)
            + np.roll(np.roll(self.grid, -1, 0), 1, 1)
            + np.roll(np.roll(self.grid, -1, 0), -1, 1)
        )

        self.grid = ((neighbors == 3) | ((self.grid == 1) & (neighbors == 2))).astype(
            np.uint8
        )
