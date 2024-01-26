import logging
import random
import pathlib
import pygame
from .. import environment as env
from .base_sprite import BaseSprite

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)


class Asteroid(BaseSprite):
    """Is a type of obstacle"""

    width = 30
    height = 30
    velocity = 6

    rotation_speed_cw = 0
    image = pygame.image.load(
        pathlib.Path().cwd() / "resources\\graphics\\sprites\\asteroid.png"
    )

    def __init__(self, x: int = 0, y: int = 0):
        super().__init__(
            x=x,
            y=y,
            width=self.width,
            height=self.height,
            colour=pygame.Color("red"),
            can_wrap_around_screen=True,
            can_leave_screen=True,
            image=self.image,
        )
        self.nonrotated_image = pygame.transform.smoothscale(
            self.image, (self.width, self.height)
        )
        self.image = self.nonrotated_image

        self.move_in_random_direction()
        self.teleport_to_random_edge()
        self.last_rotate_time = pygame.time.get_ticks()
        self.rotation_speed_cw = random.randint(-30, 30)

    def update(self):
        super().update()
        if (pygame.time.get_ticks() - self.last_rotate_time) > 20:
            logger.debug(f"{self.direction_vector=}")
            self.direction_vector = self.direction_vector.rotate(self.rotation_speed_cw)
            self.image = pygame.transform.rotate(
                self.nonrotated_image,
                self.direction_vector.angle_to((0, 1)),
            )
            self.last_rotate_time = pygame.time.get_ticks()

    def move_in_random_direction(self):
        # Spawn with a random direction and move at constant velocity
        direction_vector = pygame.Vector2(0, 0)
        while direction_vector.magnitude() == 0:
            direction_vector = pygame.Vector2(
                random.randint(-100, 100), random.randint(-100, 100)
            )
        self.velocity_vector = direction_vector.normalize() * self.velocity

    def teleport_to_random_edge(self):
        """Teleports to a random edge of the screen, but will pick a side that has the asteroid move into the field, not out of it"""
        # Generate random coordinate on the screen, then find the spawn point opposite the velocity direction on the edge of the screen
        randx = random.randint(
            round(self.width / 2), round(env.screen_width - self.width / 2)
        )
        randy = random.randint(
            round(self.height / 2), round(env.screen_height - self.height / 2)
        )

        # spawn_vector = self.velocity_vector.normalize()*-1 + pygame.math.Vector2(randx, randy)

        # TODO - make the asteroid spawn at the edge of the screen

        # Generate random coordinate along edge of screen
        random_position = random.choice(
            [
                pygame.math.Vector2(randx, self.height / 2),
                pygame.math.Vector2(self.width / 2, randy),
            ]
        )  # somewhere along the x or y axis

        if self.velocity_vector[0] < 0:  # Moving -x, so choose right edge to spawn at
            if (
                random_position[0] == self.width / 2
            ):  # if the point selected is on the y axis
                random_position[0] = x = round(env.screen_width - self.width / 2)

        if self.velocity_vector[1] < 0:  # Moving -y, so choose bottom edge to spawn at
            if (
                random_position[1] == self.height / 2
            ):  # if the point selected is on the x axis
                random_position[1] = round(env.screen_height - self.height / 2)

        self.x = random_position[0]
        self.y = random_position[1]
        logger.debug(
            "px,py=(%d,%d), vx,vy=(%d,%d)",
            self.x,
            self.y,
            self.velocity_vector[0],
            self.velocity_vector[1],
        )
