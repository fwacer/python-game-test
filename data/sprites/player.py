import math
from dataclasses import dataclass, field
import pygame
from .. import environment as env
from . import base_sprite
import pathlib


class Player(base_sprite.BaseSprite):
    """Represents the player"""

    width = 40
    height = 60
    movement_speed = 5
    colour = pygame.Color("white")
    can_wrap_around_screen = False

    def __init__(self, x, y):
        super().__init__(
            x=x,
            y=y,
            width=self.width,
            height=self.height,
            colour=self.colour,
            can_wrap_around_screen=self.can_wrap_around_screen,
        )
        self.nonrotated_image = pygame.image.load(
            pathlib.Path().cwd() / "resources\\graphics\\sprites\\ship.png"
        ).convert_alpha()
        self.image = self.nonrotated_image

    def user_initiated_movement(self, new_direction: pygame.Vector2):
        """Add to the direction that the player will move"""
        if new_direction.magnitude() != 0:
            self.direction_vector = new_direction.normalize()
            self.velocity_vector = self.direction_vector * self.movement_speed
            # print(self.get_rotation_angle_deg())
            self.image = pygame.transform.rotate(
                self.nonrotated_image, self.rotation_angle_deg
            )
        else:
            self.velocity_vector *= 0
