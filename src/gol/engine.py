import numpy as np


class GameOfLife:
    def __init__(self, width: int, height: int, max_history=1000):
        self.width = width
        self.height = height
        self.grid = np.zeros((height, width), dtype=np.uint8)

        self.history = []
        self.max_history = max_history

    def clear(self) -> None:
        self.grid.fill(0)

    def toggle(self, x: int, y: int) -> None:
        if not (0 <= x < self.width and 0 <= y < self.height):
            return
        self._save_state()
        self.grid[y, x] = 1 - self.grid[y, x]

    def alive(self, x: int, y: int) -> bool:
        return bool(self.grid[y, x])

    def _save_state(self):
        self.history.append(self.grid.copy())
        if len(self.history) > self.max_history:
            self.history.pop(0)

    def snapshot(self):
        self._save_state()

    def step(self) -> None:
        self._save_state()

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

        self.grid = np.where(
            (neighbors == 3) | ((self.grid == 1) & (neighbors == 2)),
            1,
            0,
        ).astype(np.uint8)

    def undo(self):
        if not self.history:
            return False

        self.grid = self.history.pop()
        return True

    def set_cell(self, x, y, value):
        if not (0 <= x < self.width and 0 <= y < self.height):
            return
        self.grid[y, x] = 1 if value else 0
