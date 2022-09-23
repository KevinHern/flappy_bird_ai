# Processing
from p5 import *

# Models
from flappy_bird.artificial_intelligence.bird_agent import BirdAgent
from flappy_bird.models.track import PipeTrack

# Utils
import numpy as np
import logging
from os import getcwd
from os.path import join, split
from datetime import datetime


# Initializing constants
width = 700
height = 500

# Initializing simulation constants
population = 150
generation = 1

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
def create_agent():
    return BirdAgent(
        starting_position=bird_starting_position,
        bird_diameter=bird_diameter,
        max_height=height,
        total_pipes=number_pipes,
        closest_pipe=track.pipes_queue[0]
    )


birds = np.empty(population)
birds.fill(0)
birds = np.array(
    list(map(
        lambda x: create_agent(),
        birds
    )),
    dtype=BirdAgent
)

# Initializing game variables and constants
track_complete = False


def log_stats(fittest_bird):
    # Creating message to log
    message = "\n---END OF GENERATION {}---\n".format(generation)
    message += "Population: {}\n".format(population)
    message += "Fittest Score: {}\n".format(fittest_bird.distance)
    message += "Fittest Pipes passed: {}\n".format(fittest_bird.pipes_passed)
    message += "Track {:.2f}% completed".format(100 * fittest_bird.pipes_passed / number_pipes)

    # Logging
    logging.info(
        msg=message
    )


def setup():
    # Setting up canvas
    size(width, height)

    # Setting up logger filename
    today_date = datetime.today().strftime('%Y_%m_%d-%H:%M')

    # Setting up logger
    logging.basicConfig(
        filename='training_log_neat-{}.log'.format(today_date),
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
        # TODO: Sort birds by distance
        fittest_bird = birds[0]

        # Log Stats
        log_stats(fittest_bird=fittest_bird)

        # TODO: Perform selection

        # TODO: Perform crossover

        # TODO: Perform Mutation

        # Increase evolutionary variables
        generation += 1

        # Reset simulation
        track.reset()
        for bird in birds:
            bird.reset(closest_pipe=track.pipes_queue[0])


# def key_pressed():
#     if ord(str(key)) > 0 and not bird.game_over:
#         bird.flap()
#     else:
#         pass


def mouse_pressed():
    loop()


if __name__ == '__main__':
    run()
