
import logging
import random
import pygame
import pygame.gfxdraw
from .. import environment as env

logger = logging.getLogger(__name__)

class Star():
    """Is a background sprite"""

    x,y = 0,0
    width = 10
    height = 15
    colour = pygame.Color(255,255,255,170)
    sprite = None

    def __init__(self, x,y, size_multiplier=1):
        self.reset()
        self.x, self.y = x,y
        self.width *= size_multiplier
        self.height *= size_multiplier
        #self.sprite = pygame.Rect(0,0, self.width, self.height)

        #self.move_in_random_direction()
        #self.teleport_to_random_edge()

    def move_in_random_direction(self):
        # Spawn with a random direction and move at constant velocity
        direction_vector = pygame.Vector2(0,0)
        while direction_vector.magnitude() == 0:
            direction_vector = pygame.Vector2(random.randint(-100,100), random.randint(-100,100))
        self.velocity_vector = direction_vector.normalize()*self.velocity

    def teleport_to_random_edge(self):
        '''Teleports to a random edge of the screen, but will pick a side that has the asteroid move into the field, not out of it'''
        # Generate random coordinate on the screen, then find the spawn point opposite the velocity direction on the edge of the screen
        randx = random.randint(round(self.width/2), round(env.screen_width-self.width/2))
        randy = random.randint(round(self.height/2), round(env.screen_height-self.height/2))

        #spawn_vector = self.velocity_vector.normalize()*-1 + pygame.math.Vector2(randx, randy)

        # TODO - make the asteroid spawn at the edge of the screen

        # Generate random coordinate along edge of screen
        random_position = random.choice([pygame.math.Vector2(randx, self.height/2), pygame.math.Vector2(self.width/2, randy)]) # somewhere along the x or y axis
        
        if self.velocity_vector[0] < 0: # Moving -x, so choose right edge to spawn at
            if random_position[0] == self.width/2: # if the point selected is on the y axis
                random_position[0] = x=round(env.screen_width-self.width/2)


        if self.velocity_vector[1] < 0: # Moving -y, so choose bottom edge to spawn at
            if random_position[1] == self.height/2: # if the point selected is on the x axis
                random_position[1] = round(env.screen_height-self.height/2)

        self.x = random_position[0]
        self.y = random_position[1]
        logger.debug("px,py=(%d,%d), vx,vy=(%d,%d)", self.x, self.y, self.velocity_vector[0], self.velocity_vector[1])

    def update(self, stay_on_screen: bool = False):
        #self.x += self.velocity_vector[0]
        #self.y += self.velocity_vector[1]
        self.wrap_around_screen()


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
    
    def wrap_around_screen(self):
        if (self.x - self.width/2) > env.screen_width: # off right side
            self.x = -self.width/2
        if (self.x + self.width/2) < 0: # off left side
            self.x = env.screen_width + self.width/2
        if (self.y - self.height/2) > env.screen_height: # off bottom side
            self.y = -self.height/2
        if (self.y + self.height/2) < 0: # off top side
            self.y = env.screen_height + self.height/2

    def draw(self, window):
        #pygame.draw.rect(window, self.colour, self.sprite)
        pygame.gfxdraw.filled_ellipse(window, round(self.x), round(self.y), round(self.width), round(self.height), self.colour)
        pygame.gfxdraw.aaellipse(window, round(self.x), round(self.y), round(self.width), round(self.height), self.colour)
    
    def reset(self):
        pass
    
    '''@property
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
        self.sprite.y = value - self.height/2'''
    
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
        self.layers = []

        for multiplier in range(1,25,3):
            self.layers.append(ParallaxLayer( # Furthest layer
                [
                    Star(
                        round(env.screen_width*random.random()),
                        round(env.screen_height*random.random())
                        )
                        for _ in [0]*25
                ], 0.1*multiplier)
            )


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
        for layer in self.layers:
            layer.update()
    
    def draw(self, surface):
        for layer in self.layers:
            layer.draw(surface)
    
    def move(self, direction_vector: pygame.Vector2):
        for layer in self.layers:
            layer.move(direction_vector)

    