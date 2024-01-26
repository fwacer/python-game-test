from dataclasses import dataclass, field
import pygame
from .. import environment as env
from ..utils import project_screen_to_3d, project_3d_to_screen


@dataclass(kw_only=True)
class BaseSprite(pygame.sprite.Sprite):
    """Is the base sprite that all other sprites should be derived from"""

    width: int
    height: int
    x: int = 0
    y: int = 0
    z: int = 0
    velocity_vector: pygame.Vector2 = field(default_factory=pygame.Vector2)
    colour: pygame.Color = field(default_factory=lambda: pygame.Color(0, 0, 0, 0))
    can_leave_screen: bool = True
    can_wrap_around_screen: bool = False

    def __post_init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.update()

    @property
    def rect(self):
        return pygame.Rect(
            self.x - self.width / 2, self.y - self.height / 2, self.width, self.height
        )

    def reset(self):
        raise NotImplementedError()

    def set_movement_direction(self, new_movement_direction: pygame.Vector2):
        if new_movement_direction.magnitude() == 0:
            self.velocity_vector *= 0
        else:
            self.velocity_vector = (
                new_movement_direction.normalize() * self.velocity_vector.magnitude()
            )

    def set_velocity(self, new_velocity: pygame.Vector2):
        self.velocity_vector = pygame.Vector2(new_velocity)

    def update(self):
        """Updates sprite's position on screen using its velocity vector"""
        self.x += self.velocity_vector[0]
        self.y += self.velocity_vector[1]

        if not self.can_leave_screen:
            self.keep_within_bounds()
        if self.can_wrap_around_screen:
            self.wrap_around_screen()

    def draw(self, window):
        """Subclasses will likely override this function"""
        pygame.draw.rect(window, self.colour, self.rect)

    def move_object_relative_to_camera(
        self,
        camera_movement_vector: pygame.Vector2,
        vec_in_screen_coord_frame: bool = True,
    ):
        if vec_in_screen_coord_frame:  # vector provided is in screen coordinate frame
            camera_movement_vector_3d = project_screen_to_3d(
                camera_movement_vector, self.z
            )
            camera_movement_vector = pygame.Vector2(
                camera_movement_vector_3d.x, camera_movement_vector_3d.y
            )
        else:
            # Vector is in local coordinate frame, so we don't need to do anything
            pass
        self.x += -camera_movement_vector.x
        self.y += -camera_movement_vector.y

    def out_of_bounds(self) -> bool:
        """Checks if sprite is out of bounds. Returns boolean"""
        if (
            (self.x + self.width / 2) > env.screen_width
            or (self.x - self.width / 2) < 0
            or (self.y + self.height / 2) > env.screen_height
            or (self.y - self.height / 2) < 0
        ):
            return True
        return False

    def keep_within_bounds(self):
        """Moves sprite so that it stays within bounds"""
        if (self.x + self.width / 2) > env.screen_width:
            self.x = env.screen_width - self.width / 2
        if (self.x - self.width / 2) < 0:
            self.x = 0 + self.width / 2
        if (self.y + self.height / 2) > env.screen_height:
            self.y = env.screen_height - self.height / 2
        if (self.y - self.height / 2) < 0:
            self.y = 0 + self.height / 2

    def wrap_around_screen(self):
        """Moves sprite to the other side of the screen"""
        if (self.x - self.width / 2) > env.screen_width:  # off right side
            self.x = -self.width / 2
        if (self.x + self.width / 2) < 0:  # off left side
            self.x = env.screen_width + self.width / 2
        if (self.y - self.height / 2) > env.screen_height:  # off bottom side
            self.y = -self.height / 2
        if (self.y + self.height / 2) < 0:  # off top side
            self.y = env.screen_height + self.height / 2


if __name__ == "__main__":
    SPRITES = [
        BaseSprite(
            width=10,
            height=20,
            x=50,
            y=50,
            velocity_vector=pygame.Vector2(1, 0),
            colour=pygame.Color(255, 0, 0),
        )
    ]

    WINDOW = pygame.display.set_mode((env.screen_width, env.screen_height))
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.constants.QUIT:
                running = False
        WINDOW.fill("black")

        for sprite in SPRITES:
            sprite.update()
            sprite.draw(WINDOW)
        pygame.display.update()
    pygame.quit()
