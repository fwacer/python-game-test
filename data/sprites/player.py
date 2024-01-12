
import pygame
from .. import environment as env

class Player():
    """Represents the player"""

    width = 40
    height = 60
    velocity = 5
    colour = "white"
    sprite = None
    direction_vector = None
    velocity_vector = None

    def __init__(self, x, y):

        self.reset()
        self.sprite = pygame.Rect(x-self.width/2, y - self.height/2, self.width, self.height)
        self.direction_vector = pygame.Vector2(0,0)
        self.velocity_vector = pygame.Vector2(0,0)


    def user_initiated_movement(self, new_direction: pygame.Vector2):
        '''Add to the direction that the player will move'''
        if new_direction.magnitude() != 0:
            self.velocity_vector = new_direction.normalize()*self.velocity
        else:
            self.velocity_vector *= 0

    def update(self):
        '''update position'''
        self.x += self.velocity_vector[0]
        self.y += self.velocity_vector[1]
        self.fix_out_of_bounds()


    def out_of_bounds(self):
        # Check right side:
        if (self.x + self.width/2) > env.screen_width \
        or (self.x - self.width/2) < 0 \
        or (self.y + self.height/2) > env.screen_height \
        or (self.y - self.height/2) < 0:
            return True
        return False
    
    def fix_out_of_bounds(self):
        if (self.x + self.width/2) > env.screen_width:
            self.x = env.screen_width - self.width/2
        if (self.x - self.width/2) < 0:
            self.x = 0 + self.width/2
        if (self.y + self.height/2) > env.screen_height:
            self.y = env.screen_height - self.height/2
        if (self.y - self.height/2) < 0:
            self.y = 0 + self.height/2

    def draw(self, window):
        pygame.draw.rect(window, self.colour, self.sprite)
    
    def reset(self):
        pass
    
    @property
    def x(self):
        return self.sprite.x + self.width/2
    
    @x.setter
    def x(self, value):
        self.sprite.x = value - self.width/2
    
    @property
    def y(self):
        return self.sprite.y + self.height/2
    
    @y.setter
    def y(self, value):
        self.sprite.y = value - self.height/2
    
    