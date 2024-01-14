
import logging
import random
import pygame
import pygame.gfxdraw
from dataclasses import dataclass, field
from .. import environment as env
from .base_sprite import BaseSprite

logger = logging.getLogger(__name__)

class Star(BaseSprite):
    """Is a background sprite"""

    '''width: int = 10
    height: int = 15
    colour: pygame.Color = pygame.Color(255,255,255,170)'''
    size_multiplier = 1.0

    def __init__(self, x, y, z: int = 0, size_multiplier=1.0):
        super().__init__(x=x, y=y, z=z, width=10, height=15, colour=pygame.Color(255,255,255,170), can_wrap_around_screen=True)
        self.size_multiplier = size_multiplier if size_multiplier >= 0.1 else 0.1
        self.width = round(self.width * self.size_multiplier)
        self.height = round(self.height * self.size_multiplier)
        


    def draw(self, window):
        #pygame.draw.rect(window, self.colour, self.sprite)
        #pygame.gfxdraw.filled_ellipse(window, round(self.x), round(self.y), round(self.width), round(self.height), self.colour)
        #pygame.gfxdraw.aaellipse(window, round(self.x), round(self.y), round(self.width), round(self.height), self.colour)
        #print(self)

        x, y, width, height = round(self.x), round(self.y), round(self.width), round(self.height)
        pygame.gfxdraw.filled_ellipse(window, x, y, width, height, self.colour)
        pygame.gfxdraw.aaellipse(window, x, y, width, height, self.colour)
    
class ParallaxLayer():

    def __init__(self, sprites: list, speed: 1.0):
        self.sprites = sprites
        self.speed = speed

    def move(self, direction_vector: pygame.Vector2):
        x_move,y_move = direction_vector*self.speed
        for sprite in self.sprites:
            sprite.x += x_move
            sprite.y += y_move

    def update(self):
        for sprite in self.sprites:
            sprite.update()

    def draw(self, surface):
        for sprite in self.sprites:
            sprite.draw(surface)

class StarBackground():

    def __init__(self):
        self.sprites = []

        z_max = 200
        z_min = 50
        z_increment = 10
        for z in range(z_min,z_max,z_increment):
            for _ in range(25):
                self.sprites.append(
                    Star(
                        x=round(env.screen_width*random.random()),
                        y=round(env.screen_height*random.random()),
                        z=z+random.random()*z_increment,
                        size_multiplier=(1-z/z_max)*random.random()
                        )
                    )

        '''
        for multiplier in range(1,25,3):
            self.layers.append(ParallaxLayer( # Furthest layer
                [
                    Star(
                        x=round(env.screen_width*random.random()),
                        y=round(env.screen_height*random.random()),
                        )
                        for _ in [0]*25
                ], 0.1*multiplier)
            )
        '''

        '''
        self.layers.append(ParallaxLayer(
            [
                Star(x,y, random.random()+.3) for x,y in zip(range(round(env.screen_width/8),env.screen_width,round(env.screen_width/8)), [env.screen_height*2/5]*8)
            ], 1)
        )
        self.layers.append(ParallaxLayer(
            [
                Star(x,y, random.random()+.5) for x,y in zip(range(round(env.screen_width/10),env.screen_width,round(env.screen_width/10)), [env.screen_height*3/5]*10)
            ], 5)
        )
        self.layers.append(ParallaxLayer(
            [
                Star(x,y, random.random()+.7) for x,y in zip(range(round(env.screen_width/7),env.screen_width,round(env.screen_width/7)), [env.screen_height*4/5]*7)
            ], 15)
        )'''

        '''self.layers.append(ParallaxLayer(
            [
                Star(100, 150), Star(300, 150), Star(600, 150)
            ], 1)
        )

        self.layers.append(ParallaxLayer( # Closest layer
            [
            Star(100, 150), Star(300, 150), Star(600, 150)
            ], 2)
        )'''
    
    def update(self):
        for layer in self.sprites:
            layer.update()
    
    def draw(self, surface):
        for layer in self.sprites:
            layer.draw(surface)
    
    def move_object_relative_to_camera(self, direction_vector: pygame.Vector2):
        for sprite in self.sprites:
            sprite.move_object_relative_to_camera(direction_vector)

    