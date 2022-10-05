# Pygame stuff
import numpy as np
from pygame.display import set_mode, update
from pygame.event import get
from pygame import QUIT, quit

# Models
from flappy_bird.models.floor import GameFloor
from flappy_bird.artificial_intelligence.bird_agent import BirdAgent
from flappy_bird.models.track import PipeTrack

# Utils
from flappy_bird.utils.constants import GameImages

# AI
from neat.nn import FeedForwardNetwork
from flappy_bird.artificial_intelligence.neat_setup import NeatSetup


class FlappyBirdAI:
    def __init__(self, number_pipes):
        # Initializing constants
        self.window_dimensions = np.array([500, 800])
        self.floor_height = 700

        # Initializing simulation variables
        self.generation = 0

        # Initializing Floor and Background
        self.GAME_FLOOR = GameFloor(height=self.floor_height)
        self.background_position = np.array([0, -150])

        # Setting up Game
        self.GAME_WINDOW = set_mode(self.window_dimensions)

        # Initializing Bird constants
        self.bird_starting_position = np.array([
            self.window_dimensions[0] // 4,
            3 * self.window_dimensions[1] // 8
        ])

        # Initializing Pipe constants
        self.pipe_width = 50
        self.pipe_distance = self.pipe_width * 3.5
        self.pipe_velocity = np.array([2, 0])
        self.number_pipes = number_pipes

    # Initializing Birds
    def _create_agent(self, bird_id, genome, neural_network, closest_pipe):
        return BirdAgent(
            bird_id=bird_id,
            starting_position=self.bird_starting_position,
            bird_diameter=0,
            max_height=self.floor_height - BirdAgent.ANIMATION[0].get_height(),
            total_pipes=self.number_pipes,
            closest_pipe=closest_pipe,
            genome=genome,
            neural_network=neural_network
        )

    # Game itself
    def play(self, game_track, birds_population):
        # Create a copy
        this_generation = birds_population.copy()
        while True:
            # Dispatch events before proceeding
            for event in get():
                if event.type == QUIT:
                    quit()
                    return

            # First: Drawing Background first
            self.GAME_WINDOW.blit(GameImages.BACKGROUND, self.background_position)

            # Second: Updating and drawing pipes
            passed_pipe = game_track.draw(game_window=self.GAME_WINDOW)

            # Third: Drawing Floor
            self.GAME_FLOOR.draw(game_window=self.GAME_WINDOW)

            # Fourth: Perform Bird Action, increase score and Draw
            game_overs = 0
            for bird in birds_population:
                bird.think_and_do_something()
                bird.increase_pipe_score(passed_pipe=passed_pipe,
                                         closest_pipe=game_track.pipes_queue[0] if len(
                                             game_track.pipes_queue) > 0 else None)
                bird.draw_pygame(game_window=self.GAME_WINDOW)
                game_overs += 0 if bird.game_over else 1

            birds_population = np.array(
                list(filter(lambda bird: not bird.game_over, birds_population))
            )

            # Fifth: Update canvas
            update()

            # Sixth: Determine if all birds game over
            if game_overs == 0:
                # First: Sort birds by distance
                sorted_birds = np.array(sorted(this_generation))
                fittest_bird = sorted_birds[0]

                # Second: Log Stats
                NeatSetup.log_stats(winner_genome=fittest_bird)

                break

    # Setting up simulation
    def simulation(self, genomes, config):
        # Update simulation variables
        self.generation += 1

        # Create track
        track = PipeTrack(
            pipe_distance=self.pipe_distance,
            pipe_velocity=self.pipe_velocity,
            number_pipes=self.number_pipes,
            game_dimensions=np.array([self.window_dimensions[0], self.floor_height]),
            bird_x=self.bird_starting_position[0],
            bird_width=BirdAgent.ANIMATION[0].get_width()
        )

        # Create population
        new_generation = []
        for genome_id, genome in genomes:
            # Setting fitness to 0
            genome.fitness = 0

            # Creating bird
            brain = FeedForwardNetwork.create(genome, config)
            bird = self._create_agent(
                bird_id=genome_id,
                genome=genome,
                neural_network=brain,
                closest_pipe=track.pipes_queue[0]
            )

            # Appending bird to generation
            new_generation.append(bird)

        # Casting to numpy array
        birds = np.array(
            new_generation,
            dtype=BirdAgent
        )

        # Run the simulation
        self.play(
            game_track=track,
            birds_population=birds
        )
