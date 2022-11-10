# Pygame Stuff
from pygame.mask import from_surface

# Models
from .bird import Bird
from .pipe import DualPipe

# utils
from ..utils.constants import GameImages
import numpy as np
from math import ceil


class BirdAgent(Bird):
    ANIMATION = GameImages.BIRD_ANIMATION
    ANIMATION_TIME = 5

    def __init__(
            self,
            # Game variables
            bird_id,
            starting_position,
            bird_diameter,
            max_height,
            total_pipes,
            closest_pipe,

            # Simulation variables
            genome,
            neural_network
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

        self.bird_id = bird_id

        # Initializing game variables
        self.animation_counter = 0

        # Initializing simulation variables
        self.genome = genome
        self.brain = neural_network

    def __eq__(self, other):
        return self.genome.fitness == other.genome.fitness

    def __lt__(self, other):
        return self.genome.fitness > other.genome.fitness

    @staticmethod
    def log_stats(agent):
        message = "Pipes Passed: {}\n".format(agent.pipes_passed)
        message += "Percentage Completed: {:.2f}%\n".format(100 * agent.pipes_passed / agent.total_pipes)
        return message

    def think(self):
        # Extract inputs
        inputs = (
            # First input: Bird's Y position
            self.position[1],
            # Second input: X position of the farthest corner
            self.closest_pipe.top_pipe.position[0] + self.closest_pipe.top_pipe.width + self.bird_diameter / 2,
            # Third input: Top pipe's height,
            self.closest_pipe.top_pipe.position[1] + self.closest_pipe.top_pipe.height + self.bird_diameter / 2,
            # Fourth input: Bottom pipe's height
            self.closest_pipe.bottom_pipe.position[1] - self.bird_diameter / 2
        )

        # Forward pass of the neural network
        output = self.brain.activate(inputs)

        # Think and return the action
        if output[0] > 0.5:
            return True
        else:
            return False

    def think_and_do_something(self):
        # Think first
        will_flap = self.think()

        # Perform action
        if will_flap:
            self.flap()

        # Draw
        self.update()

    # Overriding some functions to adapt Processing to Pygame + NEAT Algorithm
    def check_collision_pygame(self):
        # Masks
        bird_mask = from_surface(BirdAgent.ANIMATION[0])
        top_pipe_mask = from_surface(DualPipe.TOP_PIPE)
        bottom_pipe_mask = from_surface(DualPipe.BOTTOM_PIPE)

        # Calculating offsets
        top_pipe_offset = np.subtract(self.closest_pipe.top_pipe.position, self.position)
        top_pipe_offset[1] = ceil(top_pipe_offset[1])

        bottom_pipe_offset = np.subtract(self.closest_pipe.bottom_pipe.position, self.position)
        bottom_pipe_offset[1] = ceil(bottom_pipe_offset[1])

        # Check collisions
        top_collision = bird_mask.overlap(top_pipe_mask, top_pipe_offset)
        bottom_collision = bird_mask.overlap(bottom_pipe_mask, bottom_pipe_offset)

        if top_collision or bottom_collision:
            self.game_over = True
            # print(self.position, top_pipe_offset, bottom_pipe_offset)

    def increase_score(self):
        self.genome.fitness += 0 if self.game_over else 0.01
        # pass

    # Overriding the fitness function
    def increase_pipe_score(self, passed_pipe, closest_pipe):
        if passed_pipe and not self.game_over:
            self.genome.fitness += 0 if self.game_over else 5
            self.closest_pipe = closest_pipe
            self.pipes_passed += 1
            self.game_over = self.pipes_passed == self.total_pipes

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
                self.game_over = True
                self.position[1] = 0

            # Check Collisions
            self.check_collision_pygame()

            # Increase distance score
            self.increase_score()

    def draw_pygame(self, game_window):
        if not self.game_over:
            # Looping between the animations
            self.animation_counter = (self.animation_counter + 1) % 20

            if self.animation_counter <= 5:
                img_to_show = BirdAgent.ANIMATION[0]
            elif self.animation_counter <= 10:
                img_to_show = BirdAgent.ANIMATION[1]
            elif self.animation_counter <= 15:
                img_to_show = BirdAgent.ANIMATION[2]
            else:
                img_to_show = BirdAgent.ANIMATION[1]

            # Draw bird
            game_window.blit(img_to_show, self.position)
