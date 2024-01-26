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
    direction_vector: pygame.Vector2 = field(
        default_factory=lambda: pygame.Vector2(0, 1)
    )
    colour: pygame.Color = field(default_factory=lambda: pygame.Color(0, 0, 0, 0))
    can_leave_screen: bool = True
    can_wrap_around_screen: bool = False
    image: pygame.Surface = None

    def __post_init__(self):
        pass

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

    def draw(self, screen: pygame.Surface, offset: pygame.Vector2):
        """Subclasses will likely override this function"""
        if self.image:
            screen.blit(self.image, offset)
        else:
            pygame.draw.rect(screen, self.colour, offset)

    def move_object_relative_to_camera(
        self,
        camera_movement_vector: pygame.Vector2 = None,
        vec_in_screen_coord_frame: bool = True,
    ):
        """Parallax correction"""
        if (
            vec_in_screen_coord_frame
        ):  # vector provided is in screen coordinate frame, need to transform into object coordinate frame
            camera_movement_vector_3d = project_screen_to_3d(
                camera_movement_vector, self.z
            )
            local_frame_movement_vector = -pygame.Vector2(
                camera_movement_vector_3d.x, camera_movement_vector_3d.y
            )
        else:
            # Vector is in object coordinate frame already, so we don't need to do anything
            local_frame_movement_vector = -camera_movement_vector
        self.x += local_frame_movement_vector.x
        self.y += local_frame_movement_vector.y

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

    @property
    def rotation_angle_deg(self):
        """Measured from the y-axis (pointed down on the screen). Positive number is CCW."""
        return self.direction_vector.angle_to(pygame.Vector2(0, 1)) + 180


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
