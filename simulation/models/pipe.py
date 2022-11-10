# Pygame
from pygame.transform import flip

# Utils
import numpy as np
from ..utils.constants import PipeOrientation
from ..utils.constants import GameImages


class Pipe:
    def __init__(self, starting_x, starting_y, width, height, pipe_orientation):
        # Positional Vector
        self.position = np.array([starting_x, starting_y])

        # Size of Pipe
        self.width = width
        self.height = height

        # Orientation (whether it is located in the top or in the bottom
        self.pipe_orientation = pipe_orientation


class DualPipe:
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
            width=DualPipe.PIPE_WIDTH,
            height=0,
            pipe_orientation=PipeOrientation.TOP
        )

        self.bottom_pipe = Pipe(
            starting_x=starting_x,
            starting_y=pipes_y[1],
            width=DualPipe.PIPE_WIDTH,
            height=0,
            pipe_orientation=PipeOrientation.BOTTOM
        )

    def translate(self, pipe_velocity):
        # Moving both pipes
        self.top_pipe.position = np.subtract(self.top_pipe.position, pipe_velocity)
        self.bottom_pipe.position = np.subtract(self.bottom_pipe.position, pipe_velocity)

    def draw(self, game_window):
        # Drawing both pipes
        game_window.blit(DualPipe.TOP_PIPE, self.top_pipe.position)
        game_window.blit(DualPipe.BOTTOM_PIPE, self.bottom_pipe.position)
