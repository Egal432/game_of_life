from dataclasses import dataclass


def world_to_screen(camera, wx, wy, cell_size):
    sx = (wx - camera.x) * (cell_size * camera.zoom)
    sy = (wy - camera.y) * (cell_size * camera.zoom)
    return int(sx), int(sy)


def screen_to_world(camera, sx, sy, cell_size):
    wx = camera.x + sx / (cell_size * camera.zoom)
    wy = camera.y + sy / (cell_size * camera.zoom)
    return int(wx), int(wy)


@dataclass
class Camera:
    x: float = 0.0  # top-left world cell
    y: float = 0.0
    zoom: float = 1.0  # scale factor

    min_zoom: float = 0.2
    max_zoom: float = 5.0

    def clamp_zoom(self) -> None:
        if self.zoom < self.min_zoom:
            self.zoom = self.min_zoom
        elif self.zoom > self.max_zoom:
            self.zoom = self.max_zoom

    def pan(self, dx: float, dy: float) -> None:
        """
        Pan in world coordinates.
        dx, dy are in world-cell units.
        """
        self.x += dx
        self.y += dy

    def zoom_by(self, factor: float) -> None:
        self.zoom *= factor
