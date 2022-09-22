# Processing
from p5 import *

# Models
from flappy_bird.models.bird import Bird
from flappy_bird.models.track import PipeTrack

# Utils
import numpy as np


# Initializing constants
width = 700
height = 500

# Initializing Bird constants
bird_starting_position = np.array([width//4, height//16])

# Initializing Bird
bird = Bird(
    starting_position=bird_starting_position,
    max_height=height,
)

# Initializing Pipe constants
pipe_width = 50
pipe_distance = pipe_width * 3.5
pipe_velocity = np.array([-2, 0])
number_pipes = 10

# Initializing Pipes
track = PipeTrack(
    pipe_distance=pipe_distance,
    pipe_velocity=pipe_velocity,
    number_pipes=number_pipes,
    max_width=width,
    max_height=height,
    pipe_width=50
)

# Initializing game variables and constants
game_over = False


def setup():
    size(width, height)


def draw():
    # Clean Canvas
    background(0)

    # Draw Pipes
    track.draw()

    # Draw Bird
    bird.draw()


def key_pressed():
    if ord(str(key)) > 0:
        bird.flap()
    else:
        pass


def mouse_pressed():
    redraw()


if __name__ == '__main__':
    run()
