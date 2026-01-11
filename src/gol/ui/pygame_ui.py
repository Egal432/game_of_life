import time

import pygame

from gol.config import ALIVE_COLOR, CELL_SIZE, DEAD_COLOR, FPS, STEP_INTERVAL


def run(game):
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
                elif event.key == pygame.K_b:
                    game.undo()
            # mouse click toggles cells
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if paused and event.button == 1:  # left click
                    mx, my = event.pos
                    x = mx // CELL_SIZE
                    y = my // CELL_SIZE
                    game.toggle(x, y)

        dt = clock.tick(FPS) / 1000.0

        while pending_steps > 0:
            game.step()
            pending_steps -= 1

        if not paused:
            sim_time_acc += dt
            while sim_time_acc >= STEP_INTERVAL:
                game.step()
                sim_time_acc -= STEP_INTERVAL
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
