"""
Author: Bryce Dombrowski
Contact: brycedombrowski.com/contact
Date: 2024-01-03

Note: press CTRL+F5 to "run without debugging", which will run "start.py" instead of the selected file
"""

import time
import random
import logging
import pathlib
import pygame
from . import environment as env
from . import sprites

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.getLogger().getEffectiveLevel())

SCREEN = pygame.display.set_mode((env.screen_width, env.screen_height))
parallax_background = None


class CameraGroup(pygame.sprite.Group):
    """

    Inspired from:
    - https://www.youtube.com/watch?v=u7LPRqrzry8
    - https://github.com/clear-code-projects/Pygame-Cameras
    """

    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        # Camera position
        self.topleft = pygame.Vector2()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2

        # Background
        self.background = pygame.image.load(env.background_image_path).convert_alpha()
        self.background_rect = self.background.get_rect(topleft=(0, 0))

        self.sprites = []

    def centre_target_camera(self, target: sprites.BaseSprite):
        self.topleft.x = target.rect.centerx - self.half_width
        self.topleft.y = target.rect.centery - self.half_height

    def update(self):
        for sprite in self.sprites:
            sprite.update()

    def draw(self, player):
        self.centre_target_camera(player)

        # Background
        background_offset = self.background_rect.topleft - self.topleft
        self.display_surface.blit(self.background, background_offset)

        # Sprites
        for sprite in self.sprites:
            offset = sprite.rect.topleft - self.topleft
            sprite.draw(self.display_surface, offset)


"""def draw(player):
    # WINDOW.blit(BACKGROUND_IMG, (0,0))
    WINDOW.fill("black")

    parallax_background.update()
    parallax_background.draw(WINDOW)
    # pygame.sprite.Group.draw(SPRITES)
    for sprite in SPRITES:
        sprite.update()
        sprite.draw(WINDOW)
    pygame.display.update()

    # Note: make parallax background stars
    # centre the ship, and fly
"""


def main():
    LOGGER.debug("Game Start")
    pygame.display.set_caption("Kuiper Belt Tactics")

    camera = CameraGroup()
    player = sprites.Player(env.screen_width / 2, env.screen_height / 2)
    camera.sprites.append(player)

    on_screen_display = sprites.OnScreenDisplay()
    camera.sprites.append(on_screen_display)

    global parallax_background
    # parallax_background = sprites.StarBackground()
    # SPRITES.append(parallax_background)

    clock = pygame.time.Clock()

    time_since_last_asteroid = 0

    running = True
    while running:
        time_since_last_asteroid += clock.tick(
            60
        )  # Add the number of ms since last tick

        if time_since_last_asteroid >= env.asteroid_spawn_frequency:
            time_since_last_asteroid = 0
            if len(camera.sprites) < 10:
                camera.sprites.append(sprites.Asteroid())

        for event in pygame.event.get():
            if event.type == pygame.constants.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c and pygame.key.get_mods() & pygame.KMOD_CTRL:
                    running = False

        keys_pressed = pygame.key.get_pressed()
        direction_vector = pygame.math.Vector2(0, 0)
        # WASD or arrow key controls
        if keys_pressed[pygame.K_UP] or keys_pressed[pygame.K_w]:
            direction_vector += pygame.Vector2(0, -1)
        if keys_pressed[pygame.K_DOWN] or keys_pressed[pygame.K_s]:
            direction_vector += pygame.Vector2(0, 1)
        if keys_pressed[pygame.K_LEFT] or keys_pressed[pygame.K_a]:
            direction_vector += pygame.Vector2(-1, 0)
        if keys_pressed[pygame.K_RIGHT] or keys_pressed[pygame.K_d]:
            direction_vector += pygame.Vector2(1, 0)

        if keys_pressed[pygame.K_ESCAPE]:
            running = False  # Exit the game
        if keys_pressed[pygame.K_r]:  # Refresh the background
            parallax_background = sprites.StarBackground()
        if keys_pressed[pygame.K_1]:  # Left click to add an asteroid
            camera.sprites.append(sprites.Asteroid(50, 50))

        player.user_initiated_movement(direction_vector)

        SCREEN.fill("#71ddee")
        camera.update()
        camera.draw(player)
        pygame.display.update()

    pygame.quit()
