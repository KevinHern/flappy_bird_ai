# Processing
from p5 import *

# Pygame
from pygame.transform import flip
from pygame.mask import from_surface

# Utils
import numpy as np
from flappy_bird.utils.constants import PipeOrientation
from flappy_bird.utils.constants import GameImages


class Pipe:
    def __init__(self, starting_x, starting_y, width, height, pipe_orientation):
        # Positional Vector
        self.position = np.array([starting_x, starting_y])

        # Size of Pipe
        self.width = width
        self.height = height

        # Orientation (whether it is located in the top or in the bottom
        self.pipe_orientation = pipe_orientation

    def draw(self):
        with push_matrix():
            translate(self.position[0], self.position[1])
            rect((0, 0), self.width, self.height)


class DualPipe:
    def __init__(self, id, starting_top_pipe, starting_bottom_pipe, pipes_width, pipes_height):
        # Setting up ID
        self.id = id

        # Initializing pipes
        self.top_pipe = Pipe(
            starting_x=starting_top_pipe[0],
            starting_y=starting_top_pipe[1],
            width=pipes_width,
            height=pipes_height[0],
            pipe_orientation=PipeOrientation.TOP
        )

        self.bottom_pipe = Pipe(
            starting_x=starting_bottom_pipe[0],
            starting_y=starting_bottom_pipe[1],
            width=pipes_width,
            height=pipes_height[1],
            pipe_orientation=PipeOrientation.BOTTOM
        )

    def translate(self, pipe_velocity):
        # Moving both pipes
        self.top_pipe.position = np.add(self.top_pipe.position, pipe_velocity)
        self.bottom_pipe.position = np.add(self.bottom_pipe.position, pipe_velocity)

    def draw(self, pipe_velocity):
        # First: Translate
        self.translate(pipe_velocity=pipe_velocity)

        # Second: Draw pipes
        self.top_pipe.draw()
        self.bottom_pipe.draw()


class DualPipePygame:
    # Setting images
    TOP_PIPE = flip(GameImages.PIPE, False, True)
    BOTTOM_PIPE = GameImages.PIPE
    PIPE_WIDTH = GameImages.PIPE.get_width()
    PIPE_HEIGHT = GameImages.PIPE.get_height()

    def __init__(self, pipe_id, starting_x, pipes_y):
        # Setting self id
        self.pipe_id = pipe_id

        # Initializing pipes
        self.top_pipe = Pipe(
            starting_x=starting_x,
            starting_y=pipes_y[0],
            width=DualPipePygame.PIPE_WIDTH,
            height=0,
            pipe_orientation=PipeOrientation.TOP
        )

        self.bottom_pipe = Pipe(
            starting_x=starting_x,
            starting_y=pipes_y[1],
            width=DualPipePygame.PIPE_WIDTH,
            height=0,
            pipe_orientation=PipeOrientation.BOTTOM
        )

    def translate(self, pipe_velocity):
        # Moving both pipes
        self.top_pipe.position = np.subtract(self.top_pipe.position, pipe_velocity)
        self.bottom_pipe.position = np.subtract(self.bottom_pipe.position, pipe_velocity)

    def draw(self, game_window):
        # Drawing both pipes
        game_window.blit(DualPipePygame.TOP_PIPE, self.top_pipe.position)
        game_window.blit(DualPipePygame.BOTTOM_PIPE, self.bottom_pipe.position)

    # def get_masks(self):
    #     return np.array([
    #         from_surface()
    #     ])
