import pygame

from gol.config import ALIVE_COLOR, CELL_SIZE, DEAD_COLOR, FPS


def run(game):
    pygame.init()

    width_px = game.width * CELL_SIZE
    height_px = game.height * CELL_SIZE

    screen = pygame.display.set_mode((width_px, height_px))
    pygame.display.set_caption("Game of Life")

    clock = pygame.time.Clock()
    running = True
    paused = False

    while running:
        # --- Event handling (quit only)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused

        if not paused:
            game.step()

        # --- Draw
        screen.fill(DEAD_COLOR)

        for y in range(game.height):
            for x in range(game.width):
                if game.alive(x, y):
                    rect = pygame.Rect(
                        x * CELL_SIZE,
                        y * CELL_SIZE,
                        CELL_SIZE,
                        CELL_SIZE,
                    )
                    screen.fill(ALIVE_COLOR, rect)

        pygame.display.flip()

        # --- Timing
        clock.tick(FPS)

    pygame.quit()
