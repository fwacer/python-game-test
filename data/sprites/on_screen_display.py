import pygame
import time
from .. import environment as env
from . import base_sprite


class OnScreenDisplay(pygame.sprite.Sprite):
    start_time = 0.0
    elapsed_time = 0.0
    font = None

    def __init__(self):
        super().__init__()
        pygame.font.init()
        self.font = pygame.font.SysFont("arial", 30)
        self.start_time = time.time()
        self.rect = pygame.Rect((1, 1, 1, 1))

    def draw(self, surface: pygame.Surface, offset=None):
        time_text = self.font.render(f"Time: {round(self.elapsed_time)}s", 1, "white")
        x = round(surface.get_width() / 100)
        y = round(surface.get_height() / 100)
        surface.blit(time_text, (x, y))

    def update(self):
        self.elapsed_time = time.time() - self.start_time

    def reset_timer(self):
        self.start_time = time.time()
