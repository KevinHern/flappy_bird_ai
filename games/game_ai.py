# Processing
import p5
from p5 import *
from vispy import app

# Models
from flappy_bird.artificial_intelligence.bird_agent import BirdAgent
from flappy_bird.models.track import PipeTrack

# Utils
import numpy as np
import logging
from os import getcwd
from os.path import join, split, dirname
from datetime import datetime
from threading import Thread

# AI
import neat


# Initializing constants
width = 700
height = 500

# Initializing simulation constants
population = 150
generation = 0
max_generations = 30

# Initializing Bird constants
bird_starting_position = np.array([width//4, height//16])
bird_diameter = 35

# Initializing Pipe constants
pipe_width = 50
pipe_distance = pipe_width * 3.5
pipe_velocity = np.array([-2, 0])
number_pipes = 2

# Initializing Pipes
track = PipeTrack(
    pipe_distance=pipe_distance,
    pipe_velocity=pipe_velocity,
    number_pipes=number_pipes,
    max_width=width,
    max_height=height,
    pipe_width=50,
    bird_diameter=bird_diameter,
    bird_x=bird_starting_position[0]
)


# Initializing Birds
def create_agent(genome, neural_network):
    return BirdAgent(
        starting_position=bird_starting_position,
        bird_diameter=bird_diameter,
        max_height=height,
        total_pipes=number_pipes,
        closest_pipe=track.pipes_queue[0],
        genome=genome,
        neural_network=neural_network
    )

birds = None




def setup():
    # Setting up canvas
    size(width, height)
    loop()

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


def draw():
    global generation

    # Clean Canvas
    background(0)

    # Draw Pipes
    passed_pipe = track.draw()

    # Birds perform an action
    for bird in birds:
        bird.think_and_do_something()

    # Only draw 4 birds
    birds[0].draw()
    birds[1].draw()
    birds[2].draw()
    birds[3].draw()

    # Increase Birds' score
    for bird in birds:
        bird.increase_pipe_score(passed_pipe=passed_pipe,
                                 closest_pipe=track.pipes_queue[0] if len(track.pipes_queue) > 0 else None)

    # Check if all birds have finished
    game_overs = np.array(
        list(map(lambda x: 0 if bird.game_over else 1, birds))
    )

    if np.sum(game_overs) == 0:
        # First: Sort birds by distance
        sorted_birds = np.array(sorted(birds))
        fittest_bird = sorted_birds[0]

        # Second: Log Stats
        log_stats(fittest_bird=fittest_bird)

        # Third: Reset track simulation
        track.reset()

        # Fourth: Quit simulation
        # for bird in birds:
        #     bird.reset(closest_pipe=track.pipes_queue[0])
        exit()


# def key_pressed():
#     if ord(str(key)) > 0 and not bird.game_over:
#         bird.flap()
#     else:
#         pass


def mouse_pressed():
    loop()


def run_simulation(genomes, config):
    global generation
    global birds

    # Update simulation variables
    generation += 1

    # Create population
    new_generation = []
    for genome_id, genome in genomes:
        # Setting fitness to 0
        genome.fitness = 0

        # Creating bird
        brain = neat.nn.FeedForwardNetwork.create(genome, config)
        bird = create_agent(
            genome=genome,
            neural_network=brain
        )

        # Appending bird to generation
        new_generation.append(bird)

    # Casting to numpy array
    birds = np.array(
        new_generation,
        dtype=BirdAgent
    )

    # Run the simulation
    run(
        sketch_setup=setup,
        sketch_draw=draw,

    )


def thread_simulation(genomes, config):
    # Setting up thread
    thread_sim = Thread(
                target=run_simulation,
                args=(genomes, config)
            )

    # Start thread
    thread_sim.start()

    # Wait for process to finish
    thread_sim.join()


def neat_setup(config_path):
    # Parsing configuration file
    config = neat.config.Config(
        neat.DefaultGenome, neat.DefaultReproduction,
        neat.DefaultSpeciesSet, neat.DefaultStagnation,
        config_path
    )

    # Creating population
    p = neat.Population(config)

    # Adding statistics and logging capabilities
    p.add_reporter(neat.StdOutReporter(True))
    p.add_reporter(neat.StatisticsReporter())
    p.add_reporter(neat.Checkpointer(10))

    # Run for up to 50 generations.
    winner = p.run(thread_simulation, max_generations)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == '__main__':
    # Obtaining the path of the configuration file
    local_dir = dirname(__file__)
    config_path = join(local_dir, '../artificial_intelligence/config-feedforward.txt')

    # Calling neat_setup
    neat_setup(config_path)
