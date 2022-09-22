# Processing
from p5 import *

# Utils
import numpy as np


def get_closest_pipe(track):
    # If there are more than 1 one pipe, just return pipe 0
    if len(track.pipes_queue) > 0:
        return track.pipes_queue[0]
    else:
        # If the track has been completed, return Null
        return None


class Bird:
    GRAVITY = np.array([0, 1])

    def __init__(
            self,
            starting_position,
            max_height,
            total_pipes
    ):
        # Position Vectors
        self.starting_position = starting_position
        self.position = starting_position

        self.max_height = max_height

        # Velocity Vectors
        self.velocity = np.empty(2)
        self.velocity.fill(0)

        self.flap_velocity = np.array([0, -10])

        # Bird constants
        self.bird_diameter = 35

        # Flags
        self.game_over = False

        # Score Variables
        self.distance = 0
        self.pipes_passed = 0

        self.total_pipes = total_pipes

    def flap(self):
        self.velocity = self.flap_velocity

    def check_collision(self, dual_pipe):
        # Get points
        points = np.array([
            # X points
            [dual_pipe.top_pipe.position[0] - self.bird_diameter / 2,
             dual_pipe.top_pipe.position[0] + dual_pipe.top_pipe.width + self.bird_diameter / 2],
            # Top Pipe Y Height
            [dual_pipe.top_pipe.position[1] + dual_pipe.top_pipe.height + self.bird_diameter / 2],
            # Bottom Pipe Y Height
            [dual_pipe.bottom_pipe.position[1] - self.bird_diameter / 2],
        ])

        # Check collision Top Pipe
        if points[0][0] <= self.position[0] <= points[0][1]:
            if points[1] >= self.position[1] or points[2] <= self.position[1]:
                self.game_over = True

    def increase_pipe_score(self, passed_pipe):
        if passed_pipe and not self.game_over:
            self.pipes_passed += 1
            print("Distance: {}\nPipe Score: {}".format(self.distance, self.pipes_passed))
            self.game_over = self.pipes_passed == self.total_pipes

    def draw(self, track):
        # Check closest pipe first
        closest_pipe = get_closest_pipe(track=track)

        if closest_pipe is not None:
            # Proceed normally
            # Calculate new velocity
            self.velocity = np.add(self.velocity, Bird.GRAVITY)

            # Calculate new position
            self.position = np.add(self.position, self.velocity)
            if self.position[1] > self.max_height:
                self.position[1] = self.max_height

            # Check Collisions
            self.check_collision(dual_pipe=closest_pipe)

            # Draw
            circle(self.position[0], self.position[1], self.bird_diameter)

            # Increase distance score
            self.distance += 1

    def reset(self):
        # Resetting vectors
        self.position = self.starting_position
        self.velocity = np.empty(2)
        self.velocity.fill(0)

        # Resetting score variables
        self.distance = 0
        self.pipes_passed = 0

        # Setting flags back to normal
        self.game_over = False
