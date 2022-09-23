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
bird_diameter = 35

# Initializing Pipe constants
pipe_width = 50
pipe_distance = pipe_width * 3.5
pipe_velocity = np.array([-2, 0])
number_pipes = 2

# Initializing Pipes
track = PipeTrack(
    pipe_distance=pipe_distance,
    pipe_velocity=pipe_velocity,
    number_pipes=number_pipes,
    max_width=width,
    max_height=height,
    pipe_width=50,
    bird_diameter=bird_diameter,
    bird_x=bird_starting_position[0]
)

# Initializing Bird
bird = Bird(
    starting_position=bird_starting_position,
    bird_diameter=bird_diameter,
    max_height=height,
    total_pipes=number_pipes,
    closest_pipe=track.pipes_queue[0]
)

# Initializing game variables and constants
track_complete = False


def setup():
    size(width, height)


def draw():
    # Clean Canvas
    background(0)

    # Draw Pipes
    passed_pipe = track.draw()

    # Draw Bird
    bird.draw()

    # Increase Bird score
    bird.increase_pipe_score(passed_pipe=passed_pipe, closest_pipe=track.pipes_queue[0] if len(track.pipes_queue)>0 else None)

    if bird.game_over:
        print("Game Over")
        track.reset()
        bird.reset(closest_pipe=track.pipes_queue[0])


def key_pressed():
    if ord(str(key)) > 0 and not bird.game_over:
        bird.flap()
    else:
        pass


def mouse_pressed():
    loop()


if __name__ == '__main__':
    run()
