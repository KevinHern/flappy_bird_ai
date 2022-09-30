# Pygame stuff
import numpy as np
from pygame.display import set_mode, update
from pygame.event import get
from pygame import QUIT, quit

# Models
from flappy_bird.models.floor import GameFloor
from flappy_bird.artificial_intelligence.bird_agent import BirdAgent
from flappy_bird.models.track import PipeTrackPygame

# Utils
import logging
from datetime import datetime
from flappy_bird.utils.constants import GameImages

# AI
from flappy_bird.artificial_intelligence.neat_setup import restore_population_checkpoint
from neat.nn import FeedForwardNetwork


# Initializing constants
window_dimensions = np.array([500, 800])
floor_height = 700

# Initializing simulation constants
generation = 0
max_generations = 1

# Initializing Floor and Background
GAME_FLOOR = GameFloor(height=floor_height)
background_position = np.array([0, -150])

# Setting up Game
GAME_WINDOW = set_mode(window_dimensions)

# Initializing Bird constants
bird_starting_position = np.array([
    window_dimensions[0]//4,
    3*window_dimensions[1]//8
])

# Initializing Pipe constants
pipe_width = 50
pipe_distance = pipe_width * 3.5
pipe_velocity = np.array([2, 0])
number_pipes = 2


# Initializing Birds
def create_agent(bird_id, genome, neural_network, closest_pipe):
    return BirdAgent(
        bird_id=bird_id,
        starting_position=bird_starting_position,
        bird_diameter=0,
        max_height=floor_height - BirdAgent.ANIMATION[0].get_height(),
        total_pipes=number_pipes,
        closest_pipe=closest_pipe,
        genome=genome,
        neural_network=neural_network
    )


def log_stats(fittest_bird):
    # Creating message to log
    message = "\n---END OF GENERATION {}---\n".format(generation)
    message += "Fittest Score: {}\n".format(fittest_bird.genome.fitness)
    message += "Fittest Pipes passed: {}\n".format(fittest_bird.pipes_passed)
    message += "Track {:.2f}% completed".format(100 * fittest_bird.pipes_passed / number_pipes)

    # Logging
    logging.info(
        msg=message
    )


def play(game_track, birds_population):
    # Create a copy
    this_generation = birds_population.copy()
    while True:
        # Dispatch events before proceeding
        for event in get():
            if event.type == QUIT:
                quit()
                return

        # First: Drawing Background first
        GAME_WINDOW.blit(GameImages.BACKGROUND, background_position)

        # Second: Updating and drawing pipes
        passed_pipe = game_track.draw(game_window=GAME_WINDOW)

        # Third: Drawing Floor
        GAME_FLOOR.draw(game_window=GAME_WINDOW)

        # Fourth: Perform Bird Action, increase score and Draw
        game_overs = 0
        for bird in birds_population:
            bird.think_and_do_something()
            bird.increase_pipe_score(passed_pipe=passed_pipe,
                                     closest_pipe=game_track.pipes_queue[0] if len(game_track.pipes_queue) > 0 else None)
            bird.draw_pygame(game_window=GAME_WINDOW)
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
            log_stats(fittest_bird=fittest_bird)

            break


def simulation(genomes, config):
    global generation

    # Update simulation variables
    generation += 1

    # Create track
    track = PipeTrackPygame(
        pipe_distance=pipe_distance,
        pipe_velocity=pipe_velocity,
        number_pipes=number_pipes,
        game_dimensions=np.array([window_dimensions[0], floor_height]),
        bird_x=bird_starting_position[0],
        bird_width=BirdAgent.ANIMATION[0].get_width()
    )

    # Create population
    new_generation = []
    for genome_id, genome in genomes:
        # Setting fitness to 0
        genome.fitness = 0

        # Creating bird
        brain = FeedForwardNetwork.create(genome, config)
        bird = create_agent(
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
    play(
        game_track=track,
        birds_population=birds
    )


if __name__ == '__main__':
    # Setup Logger
    # Setting up logger filename
    today_date = datetime.today().strftime('%Y_%m_%d-%H_%M')

    # Setting up logger
    logging.basicConfig(
        filename='training_log_neat_{}.log'.format(today_date),
        filemode='w',
        level=logging.INFO,
        format='\n%(asctime)s-%(levelname)s> %(message)s',
        datefmt='%d-%b-%y %H:%M:%S'
    )

    # Calling neat_setup
    restore_population_checkpoint(
        simulation=simulation,
        max_generations=max_generations,
        checkpoint_number=49
    )

