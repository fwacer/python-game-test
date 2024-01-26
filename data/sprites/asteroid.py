import logging
import random
import pygame
from .. import environment as env

logger = logging.getLogger(__name__)


class Asteroid:
    """Is a type of obstacle"""

    width = 30
    height = 30
    velocity = 6
    colour = "red"
    sprite = None
    velocity_vector = None

    def __init__(self):
        self.reset()
        self.sprite = pygame.Rect(0, 0, self.width, self.height)

        self.move_in_random_direction()
        self.teleport_to_random_edge()

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

    def update(self, stay_on_screen: bool = False):
        self.x += self.velocity_vector[0]
        self.y += self.velocity_vector[1]

        if stay_on_screen:
            self.fix_out_of_bounds()

    def out_of_bounds(self):
        # Check right side:
        if (
            (self.x + self.width / 2) > env.screen_width
            or (self.x - self.width / 2) < 0
            or (self.y + self.height / 2) > env.screen_height
            or (self.y - self.height / 2) < 0
        ):
            return True
        return False

    def fix_out_of_bounds(self):
        if (self.x + self.width / 2) > env.screen_width:
            self.x = env.screen_width - self.width / 2
        if (self.x - self.width / 2) < 0:
            self.x = 0 + self.width / 2
        if (self.y + self.height / 2) > env.screen_height:
            self.y = env.screen_height - self.height / 2
        if (self.y - self.height / 2) < 0:
            self.y = 0 + self.height / 2

    def draw(self, window):
        pygame.draw.rect(window, self.colour, self.sprite)

    def reset(self):
        pass

    @property
    def x(self):
        return self.sprite.x + self.width / 2

    @x.setter
    def x(self, value):
        self.sprite.x = value - self.width / 2

    @property
    def y(self):
        return self.sprite.y + self.height / 2

    @y.setter
    def y(self, value):
        self.sprite.y = value - self.height / 2
