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

WINDOW = pygame.display.set_mode((env.screen_width, env.screen_height))
BACKGROUND_IMG = pygame.image.load(env.background_image_path)
SPRITES = []

def draw(player):
    WINDOW.blit(BACKGROUND_IMG, (0,0))

    for sprite in SPRITES:
        sprite.update()
        sprite.draw(WINDOW)
    pygame.display.update()

def main():
    LOGGER.debug("Game Start")
    pygame.display.set_caption("asteroids-clone")

    player = sprites.Player(200, env.screen_height)
    SPRITES.append(player)

    on_screen_display = sprites.OnScreenDisplay()
    SPRITES.append(on_screen_display)

    clock = pygame.time.Clock()

    time_since_last_asteroid = 0

    running = True
    while running:
        time_since_last_asteroid += clock.tick(60) # Add the number of ms since last tick

        if time_since_last_asteroid >= env.asteroid_spawn_frequency:
            time_since_last_asteroid = 0
            SPRITES.append(sprites.Asteroid())


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break

        keys_pressed = pygame.key.get_pressed()
        direction_vector = pygame.math.Vector2(0,0)
        if keys_pressed[pygame.K_LEFT]:
            direction_vector += pygame.Vector2(-1,0)
        if keys_pressed[pygame.K_RIGHT]:
            direction_vector += pygame.Vector2(1,0)
        if keys_pressed[pygame.K_UP]:
            direction_vector += pygame.Vector2(0,-1)
        if keys_pressed[pygame.K_DOWN]:
            direction_vector += pygame.Vector2(0,1)
        if keys_pressed[pygame.K_ESCAPE]:
            running = False # Exit the game
        if keys_pressed[pygame.K_1]:
            SPRITES.append(sprites.Asteroid())
        
        player.user_initiated_movement(direction_vector)

        draw(SPRITES)
    
    pygame.quit()

