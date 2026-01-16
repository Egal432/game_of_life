
import math

import numpy as np
import pygame

from gol.config import (ALIVE_COLOR, CELL_SIZE, DEAD_COLOR, FPS, MAX_STEP,
                        MIN_STEP, POINT_COLOR, STEP_INTERVAL)
from gol.ui.camera import Camera, screen_to_world, world_to_screen


def run(game):
    # --- Helper to mark future as dirty
    def mark_future_dirty():
        nonlocal future_sim_dirty, future_surface_dirty
        future_sim_dirty = True
        future_surface_dirty = True

    # --- Camera
    camera = Camera(x=0.0, y=0.0, zoom=1.0)

    SCREEN_W, SCREEN_H = 900, 900
    ALPHA_SCALE = 0.75
    SIMUL_RANGE = 25
    
    step_interval = STEP_INTERVAL
    dragging = False
    drag_value = None
    dragged_cells = set()

    future_surface_dirty = True
    future_sim_dirty = True
    show_future = False

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
    pygame.display.set_caption("Game of Life")

    # Preallocate future surface
    future_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA)

    clock = pygame.time.Clock()
    paused = False
    pending_steps = 0
    sim_time_acc = 0.0
    running = True

    while running:
        dt = clock.tick(FPS) / 1000.0

        # --- Event handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    paused = not paused
                elif event.key == pygame.K_n and paused:
                    pending_steps += 1
                elif event.key == pygame.K_b and paused:
                    game.undo()
                    mark_future_dirty()
                elif event.key == pygame.K_f:
                    show_future = not show_future
                    mark_future_dirty()

                   #Adjust step speed 
                elif event.key in (pygame.K_PLUS, pygame.K_EQUALS):
                    step_interval = max(MIN_STEP, step_interval * 0.8) 
                elif event.key == pygame.K_MINUS:
                    step_interval = min(MAX_STEP, step_interval * 1.25)
                elif event.key == pygame.K_c:
                    game.clear()
                    mark_future_dirty()

            # Mouse click / dragging
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if paused and event.button in (1, 3):
                    mx, my = event.pos
                    wx, wy = screen_to_world(camera, mx, my, CELL_SIZE)
                    x, y = int(wx), int(wy)
                    if 0 <= x < game.width and 0 <= y < game.height:
                        dragging = True
                        drag_value = event.button == 1
                        game.snapshot()
                        game.set_cell(x, y, drag_value)
                        dragged_cells.clear()
                        mark_future_dirty()

            elif event.type == pygame.MOUSEMOTION:
                if paused and dragging:
                    mx, my = event.pos
                    wx, wy = screen_to_world(camera, mx, my, CELL_SIZE)
                    x, y = int(wx), int(wy)
                    if 0 <= x < game.width and 0 <= y < game.height:
                        if (x, y) not in dragged_cells:
                            game.set_cell(x, y, drag_value)
                            dragged_cells.add((x, y))
                            mark_future_dirty()

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button in (1, 3):
                    dragging = False
                    drag_value = None
                    mark_future_dirty()

            elif event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    camera.zoom_by(1.1)
                elif event.y < 0:
                    camera.zoom_by(0.9)
                mark_future_dirty()

        # --- Keyboard pan ---
        keys = pygame.key.get_pressed()
        pan_speed = 1 / camera.zoom
        if keys[pygame.K_w]:
            camera.pan(0, -pan_speed)
            mark_future_dirty()
        if keys[pygame.K_s]:
            camera.pan(0, pan_speed)
            mark_future_dirty()
        if keys[pygame.K_a]:
            camera.pan(-pan_speed, 0)
            mark_future_dirty()
        if keys[pygame.K_d]:
            camera.pan(pan_speed, 0)
            mark_future_dirty()

        # --- Simulation stepping ---
        # Manual steps
        while pending_steps > 0:
            game.step()
            mark_future_dirty()
            pending_steps -= 1

        # Automatic stepping
        if not paused:
            sim_time_acc += dt
            while sim_time_acc >= step_interval:  # step_interval
                game.step()
                mark_future_dirty()
                sim_time_acc -= step_interval

        # --- Simulate future if needed ---
        if show_future and future_sim_dirty:
            game.simulate(SIMUL_RANGE)
            future_sim_dirty = False
            future_surface_dirty = True

        # --- Compute visible range ---
        screen_w, screen_h = screen.get_size()
        cell_px = CELL_SIZE * camera.zoom
        visible_cols = int(screen_w / cell_px) + 2
        visible_rows = int(screen_h / cell_px) + 2
        start_x = max(0, int(camera.x))
        start_y = max(0, int(camera.y))
        end_x = min(game.width, start_x + visible_cols)
        end_y = min(game.height, start_y + visible_rows)
        cell_px = int(round(cell_px))

        # --- Draw background ---
        screen.fill(DEAD_COLOR)

        # --- Draw future using numpy surfarray for speed ---
        if show_future and future_surface_dirty:
            future_surface.fill((0, 0, 0, 0))
            arr = np.zeros((screen_h, screen_w, 4), dtype=np.uint8)

            for step_idx, grid in enumerate(game.future_states):
                alpha = int(255 * ALPHA_SCALE * (1.0 - step_idx / len(game.future_states)))
                color = (*ALIVE_COLOR[:3], alpha)

                # Only alive cells
                ys, xs = np.nonzero(grid)
                for y_cell, x_cell in zip(ys, xs):
                    if start_x <= x_cell < end_x and start_y <= y_cell < end_y:
                        sx, sy = world_to_screen(camera, x_cell, y_cell, CELL_SIZE)
                        sx, sy = int(sx), int(sy)
                        if 0 <= sx < screen_w and 0 <= sy < screen_h:
                            sx, sy = world_to_screen(camera, x_cell, y_cell, CELL_SIZE)
                            sx, sy = int(sx), int(sy)
                            rect = pygame.Rect(sx,
                                               sy,
                                               int(CELL_SIZE*camera.zoom)+1,
                                               int(CELL_SIZE*camera.zoom)+1)
                            pygame.draw.rect(future_surface, color, rect)
            future_surface_dirty = False

        if show_future:
            screen.blit(future_surface, (0, 0))

        # --- Draw live cells ---
        ys, xs = np.nonzero(game.grid)
        for y_cell, x_cell in zip(ys, xs):
            if start_x <= x_cell < end_x and start_y <= y_cell < end_y:
                sx, sy = world_to_screen(camera, x_cell, y_cell, CELL_SIZE)
                rect = pygame.Rect(int(sx), int(sy), cell_px + 1, cell_px + 1)
                pygame.draw.rect(screen, ALIVE_COLOR, rect)

        # Optional: draw grid dots if zoomed in
        if camera.zoom >= 0.8:
            for y_cell, x_cell in zip(ys, xs):
                if start_x <= x_cell < end_x and start_y <= y_cell < end_y:
                    sx, sy = world_to_screen(camera, x_cell + 0.5, y_cell + 0.5, CELL_SIZE)
                    screen.set_at((int(sx), int(sy)), POINT_COLOR)

        pygame.display.flip()

    pygame.quit()
