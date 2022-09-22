# Processing
from p5 import *

# Utils
import numpy as np


class Bird:
    GRAVITY = np.array([0, 1])

    def __init__(
            self,
            starting_position,
            max_height
    ):
        # Position Vectors
        self.position = starting_position

        self.max_height = max_height

        # Velocity Vectors
        self.velocity = np.empty(2)
        self.velocity.fill(0)

        self.flap_velocity = np.array([0, -10])

        # Bird constants
        self.bird_radius = 35

    def flap(self):
        self.velocity = self.flap_velocity

    def draw(self):
        # Calculate new velocity
        self.velocity = np.add(self.velocity, Bird.GRAVITY)

        # Calculate new position
        self.position = np.add(self.position, self.velocity)
        print(self.position, self.max_height)
        if self.position[1] > self.max_height:
            self.position[1] = self.max_height

        # Draw
        circle(self.position[0], self.position[1], self.bird_radius)
