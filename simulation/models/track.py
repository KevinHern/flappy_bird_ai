# Models
from .pipe import DualPipe

# Utils
import numpy as np
from math import ceil
from random import uniform


class PipeTrack:
    def __init__(
            self,
            pipe_distance, pipe_velocity, number_pipes,
            game_dimensions,
            bird_x, bird_width
    ):
        # Initializing constants
        self.game_window_dimensions = game_dimensions

        self.pipe_distance = ceil((pipe_distance + DualPipe.PIPE_WIDTH) * 1.05)
        self.pipe_velocity = pipe_velocity
        self.number_pipes = number_pipes
        self.pipes_gap = 5 * self.game_window_dimensions[1] // 16

        self.pipe_0_threshold = bird_x - DualPipe.PIPE_WIDTH + (bird_width // 2)

        # Creating empty track
        self.pipes_track = None

        # Creating random raw Pipe track
        self.create_random_track()

        # Lazy Loading
        self.number_pipes_to_display = self.game_window_dimensions[0] // self.pipe_distance
        self.pipes_queue = np.array([self.pipes_track[0]])
        self.next_pipe_counter = self.pipe_distance
        self.next_pipe = 1

        # Setting flags
        self.track_complete = False

    def create_random_track(self):
        # Creating random raw Pipe track
        dual_pipes = []
        for pipe in range(self.number_pipes):
            # Both pipes start at the edge of the screen
            starting_x = self.game_window_dimensions[0]

            # Calculating Pipes Height
            top_pipe_y = -DualPipe.PIPE_HEIGHT + ceil(self.game_window_dimensions[1] * uniform(0.05, 0.60))
            bottom_pipe_y = DualPipe.PIPE_HEIGHT + top_pipe_y + self.pipes_gap
            # top_pipe_y = -DualPipePygame.PIPE_HEIGHT - 200
            # bottom_pipe_y = DualPipePygame.PIPE_HEIGHT

            # Creating Dual Pipe
            dual_pipe = DualPipe(
                pipe_id=pipe,
                starting_x=starting_x,
                pipes_y=np.array([top_pipe_y, bottom_pipe_y]),
            )

            # Appending to track
            dual_pipes.append(dual_pipe)

        self.pipes_track = np.array(dual_pipes)

    def add_pipe_to_queue(self):
        # Obtain new pipe and add it to queue
        self.pipes_queue = np.append(self.pipes_queue, self.pipes_track[self.next_pipe])

        # Increase next pipe counter
        self.next_pipe += 1

        # Set flag
        self.track_complete = self.next_pipe == self.number_pipes

    def draw(self, game_window):
        # Translate pipes first
        for pipes in self.pipes_queue:
            pipes.translate(pipe_velocity=self.pipe_velocity)

        # Decrease next pipe counter
        self.next_pipe_counter -= self.pipe_velocity[0]

        # Add next pipe
        if self.next_pipe_counter <= 0 and not self.track_complete:
            self.add_pipe_to_queue()

            # Reset counter
            self.next_pipe_counter = self.pipe_distance

        # Check first pipe's x position
        passed_pipe = False
        if len(self.pipes_queue) > 0 and self.pipes_queue[0].top_pipe.position[0] <= self.pipe_0_threshold:
            # Pop first dual pipe
            self.pipes_queue = self.pipes_queue[1:]
            passed_pipe = True

        # Draw pipes
        for dual_pipe in self.pipes_queue:
            dual_pipe.draw(game_window=game_window)

        return passed_pipe

    def reset(self):
        # Creating track again
        self.create_random_track()

        # Reset Lazy loading
        self.pipes_queue = np.array([self.pipes_track[0]])
        self.next_pipe_counter = self.pipe_distance
        self.next_pipe = 1

        # Setting flags
        self.track_complete = False
