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
    GRAVITY = np.array([0, 0.25])

    def __init__(
            self,
            starting_position,
            bird_diameter,
            max_height,
            total_pipes,
            closest_pipe
    ):
        # Position Vectors
        self.starting_position = starting_position
        self.position = starting_position

        self.max_height = max_height

        # Velocity Vectors
        self.velocity = np.empty(2)
        self.velocity.fill(0)

        self.flap_velocity = np.array([0, -8])

        # Bird constants
        self.bird_diameter = bird_diameter
        self.bird_radius = bird_diameter / 2
        self.closest_pipe = closest_pipe

        # Flags
        self.game_over = False

        # Score Variables
        self.distance = 0
        self.pipes_passed = 0

        self.total_pipes = total_pipes

    def flap(self):
        self.velocity = self.flap_velocity

    def check_collision(self):
        # Get points
        points = np.array([
            # X points
            [self.closest_pipe.top_pipe.position[0] - self.bird_radius,
             self.closest_pipe.top_pipe.position[0] + self.closest_pipe.top_pipe.width + self.bird_radius],
            # Top Pipe Y Height
            [self.closest_pipe.top_pipe.position[1] + self.closest_pipe.top_pipe.height + self.bird_radius],
            # Bottom Pipe Y Height
            [self.closest_pipe.bottom_pipe.position[1] - self.bird_radius],
        ])

        # Check collision Top Pipe
        if points[0][0] <= self.position[0] <= points[0][1]:
            if points[1] >= self.position[1] or points[2] <= self.position[1]:
                self.game_over = True

    def increase_pipe_score(self, passed_pipe, closest_pipe):
        if passed_pipe and not self.game_over:
            self.pipes_passed += 1
            print("Distance: {}\nPipe Score: {}".format(self.distance, self.pipes_passed))
            self.closest_pipe = closest_pipe
            self.game_over = self.pipes_passed == self.total_pipes

    def increase_score(self):
        self.distance += 1

    def update(self):
        if self.closest_pipe is not None:
            # Proceed normally
            # Calculate new velocity
            self.velocity = np.add(self.velocity, Bird.GRAVITY)

            # Calculate new position
            self.position = np.add(self.position, self.velocity)

            if self.position[1] > self.max_height:
                self.game_over = True
                self.position[1] = self.max_height
            if self.position[1] < 0:
                self.position[1] = 0

            # Check Collisions
            self.check_collision()

            # Increase distance score
            self.increase_score()

    def draw(self):
        # Draw
        circle(self.position[0], self.position[1], self.bird_diameter)

    def reset(self, closest_pipe):
        # Resetting vectors
        self.position = self.starting_position
        self.velocity = np.empty(2)
        self.velocity.fill(0)

        # Resetting score variables
        self.distance = 0
        self.pipes_passed = 0

        # Setting flags back to normal
        self.game_over = False

        # Set new closest pipe
        self.closest_pipe = closest_pipe
