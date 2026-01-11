import time

import pygame

from gol.config import (
    ALIVE_COLOR,
    CELL_SIZE,
    DEAD_COLOR,
    FPS,
    MAX_STEP,
    MIN_STEP,
    STEP_INTERVAL,
)


def run(game):
    step_interval = 0.2
    MIN_STEP = 0.02
    MAX_STEP = 1.0

    dragging = False
    drag_value = None
    dragged_cells = set()

    pygame.init()

    width_px = game.width * CELL_SIZE
    height_px = game.height * CELL_SIZE

    screen = pygame.display.set_mode((width_px, height_px))
    pygame.display.set_caption("Game of Life")

    clock = pygame.time.Clock()

    paused = False
    pending_steps = 0
    sim_time_acc = 0.0

    running = True

    while running:
        # --- Events
        for event in pygame.event.get():
            # closing window
            if event.type == pygame.QUIT:
                running = False

            # Spacebar = Pause
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused

                # n press = 1 step
                elif event.key == pygame.K_n and paused:
                    pending_steps += 1

                # simple undo with history of 1000 ~ 10 mb max
                elif event.key == pygame.K_b and paused:
                    game.undo()

                elif event.key in (pygame.K_PLUS, pygame.K_EQUALS):
                    step_interval = max(MIN_STEP, step_interval * 0.8)

                elif event.key == pygame.K_MINUS:
                    step_interval = min(MAX_STEP, step_interval * 1.25)

            # mouse click toggles cells, dragging draws cells
            # left mouse = alive, right mouse = unalive
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if paused and event.button in (1, 3):

                    mx, my = event.pos
                    x = mx // CELL_SIZE
                    y = my // CELL_SIZE

                    dragging = True
                    drag_value = event.button == 1
                    game.snapshot()

                    game.set_cell(x, y, drag_value)
                    dragged_cells.clear()

            elif event.type == pygame.MOUSEMOTION:
                if paused and dragging:
                    mx, my = event.pos
                    x = mx // CELL_SIZE
                    y = my // CELL_SIZE

                    if (x, y) not in dragged_cells:
                        game.set_cell(x, y, drag_value)
                        dragged_cells.add((x, y))

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button in (1, 3):
                    dragging = False
                    drag_value = None

        dt = clock.tick(FPS) / 1000.0

        # manual steps: instant, uncapped
        while pending_steps > 0:
            game.step()
            pending_steps -= 1

        # automatic stepping when unpaused
        if not paused:
            sim_time_acc += dt
            while sim_time_acc >= step_interval:
                game.step()
                sim_time_acc -= step_interval
        else:
            for _ in range(pending_steps):
                game.step()
            pending_steps = 0

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
