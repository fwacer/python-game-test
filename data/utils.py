import logging
import random
import numpy
import pygame
from . import environment as env


class Matrix_3x3:
    def __init__():
        pass


def project_3d_to_screen(vec3: pygame.Vector3) -> pygame.Vector2:
    """Projects from 3D space to 2D space (ie: to the screen)"""
    # camera is behind the screen at distance env.camera_distance_from_screen_px
    z0 = env.camera_distance_from_screen_px
    return vec3 * (z0 + vec3.z) / z0


def project_screen_to_3d(vec2: pygame.Vector2, destination_z) -> pygame.Vector3:
    """Projects a vector from 2D space to 3D space. (ie: from the screen to a given depth)"""
    z0 = env.camera_distance_from_screen_px
    vec2 *= z0 / (z0 + destination_z)
    return pygame.Vector3(vec2.x, vec2.y, destination_z)
