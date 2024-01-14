
import pathlib
import math
screen_width, screen_height = 1000,800

# Camera FOV is estimated to be 84 degrees for width (1.47rad). 
# h = w / (2 * tan(84 degrees / 2 * pi/180))
camera_distance_from_screen_px = round(screen_width / 2.0 / math.tan(84/2 * math.pi/180)) # Used for calculating the size and speed of 3D objects projected to the screen

background_image_path = pathlib.Path('.\\resources\\graphics\\backgrounds\\space_purple.png').absolute()

asteroid_spawn_frequency = 1000


