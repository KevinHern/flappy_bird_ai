# Models
import numpy as np

from flappy_bird.models.bird import Bird

# utils
from random import choice


class BirdAgent(Bird):
    def __init__(
            self,
            starting_position,
            bird_diameter,
            max_height,
            total_pipes,
            closest_pipe
    ):
        # Initializing parent fields
        super(
            BirdAgent,
            self,
        ).__init__(
            starting_position=starting_position,
            bird_diameter=bird_diameter,
            max_height=max_height,
            total_pipes=total_pipes,
            closest_pipe=closest_pipe
        )

    def think(self):
        # Extract inputs
        inputs = np.array([
            # First input: Bird's Y position
            self.position[1],
            # Second input: X position of the farthest corner
            self.closest_pipe.top_pipe.position[0] + self.closest_pipe.top_pipe.width + self.bird_diameter / 2,
            # Third input: Top pipe's height,
            self.closest_pipe.top_pipe.position[1] + self.closest_pipe.top_pipe.height + self.bird_diameter / 2,
            # Fourth input: Bottom pipe's height
            self.closest_pipe.bottom_pipe.position[1] - self.bird_diameter / 2
        ])

        # TODO: Forward pass of the neural network

        # Think and return the action
        return choice([True, False])

    def think_and_do_something(self):
        # Think first
        will_flap = self.think()

        # Perform action
        if will_flap:
            self.flap()

        # Draw
        self.update()


