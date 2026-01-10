class GameOfLife:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid = [
            [False for _ in range(width)]
            for _ in range(height)
        ]

    def clear(self) -> None:
        for y in range(self.height):
            for x in range(self.width):
                self.grid[y][x] = False

    def toggle(self, x: int, y: int) -> None:
        self.grid[y][x] = not self.grid[y][x]

    def alive(self, x: int, y: int) -> bool:
        return self.grid[y][x]

    def step(self) -> None:
        new_grid = [
            [False for _ in range(self.width)]
            for _ in range(self.height)
        ]

        for y in range(self.height):
            for x in range(self.width):
                neighbors = self._count_neighbors(x, y)
                alive = self.grid[y][x]

                if alive and neighbors in (2, 3):
                    new_grid[y][x] = True
                elif not alive and neighbors == 3:
                    new_grid[y][x] = True

        self.grid = new_grid

    def _count_neighbors(self, x: int, y: int) -> int:
        count = 0

        for dy in (-1, 0, 1):
            for dx in (-1, 0, 1):
                if dx == 0 and dy == 0:
                    continue

                nx = (x + dx) % self.width
                ny = (y + dy) % self.height

                if self.grid[ny][nx]:
                    count += 1

        return count

