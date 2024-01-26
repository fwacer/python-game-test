import pygame
import time
from .. import environment as env


class OnScreenDisplay:
    start_time = 0.0
    elapsed_time = 0.0
    font = None

    def __init__(self):
        pygame.font.init()
        self.font = pygame.font.SysFont("arial", 30)
        self.start_time = time.time()

    def draw(self, window: pygame.Surface):
        time_text = self.font.render(f"Time: {round(self.elapsed_time)}s", 1, "white")
        x = round(window.get_width() / 100)
        y = round(window.get_height() / 100)
        window.blit(time_text, (x, y))

    def update(self):
        self.elapsed_time = time.time() - self.start_time

    def reset_timer(self):
        self.start_time = time.time()
