# utils
from os.path import join, dirname

# AI
import neat
from flappy_bird.games.visualize import *
from flappy_bird.neat_converter.genome_to_json import *

NEAT_CHECKPOINT = 10


def neat_setup(simulation, max_generations):
    # Obtaining the path of the configuration file
    local_dir = dirname(__file__)
    config_path = join(local_dir, '../artificial_intelligence/config-feedforward.txt')

    # Parsing configuration file
    config = neat.config.Config(
        neat.DefaultGenome, neat.DefaultReproduction,
        neat.DefaultSpeciesSet, neat.DefaultStagnation,
        config_path
    )

    # Creating population
    generation = neat.Population(config)

    # Adding statistics and logging capabilities
    generation.add_reporter(neat.StdOutReporter(True))
    generation.add_reporter(neat.StatisticsReporter())
    generation.add_reporter(neat.Checkpointer(NEAT_CHECKPOINT))

    # Run for up to max_generations generations.
    winner = generation.run(simulation, max_generations)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))


def restore_population_checkpoint(simulation, max_generations, checkpoint_number):
    # Obtaining the path of the configuration file
    local_dir = dirname(dirname(__file__))
    config_path = join(local_dir, 'artificial_intelligence', 'config-feedforward.txt')

    # Parsing configuration file
    config = neat.config.Config(
        neat.DefaultGenome, neat.DefaultReproduction,
        neat.DefaultSpeciesSet, neat.DefaultStagnation,
        config_path
    )

    # Obtaining the path of the checkpoint
    local_dir = dirname(dirname(__file__))
    checkpoint_path = join(local_dir, 'games', 'neat-checkpoint-{}'.format(checkpoint_number))
    print(checkpoint_path)

    # Creating population
    generation = neat.Checkpointer.restore_checkpoint(checkpoint_path)

    # Adding statistics and logging capabilities
    generation.add_reporter(neat.StdOutReporter(True))
    generation.add_reporter(neat.StatisticsReporter())

    # Run for up to max_generations generations.
    winner = generation.run(simulation, max_generations)

    # show final stats
    print('\nType of Variable: {}\nBest genome:\n{!s}'.format(type(winner), winner))

    # Save Neural Network
    local_dir = dirname(dirname(__file__))
    filename = join(local_dir, 'artificial_intelligence', 'neural_network.json')

    convert_genome_to_json(
        filename=filename,
        genome=winner,
        config=config,
        inputs_name=[
            "Bird Y Position",
            "X position of the farthest corner",
            "Top pipe's height",
            "Bottom pipe's height",
        ],
        outputs_name=["Flap"]
    )

    # result = draw_net(
    #     config=config,
    #     genome=winner,
    #     view=True,
    # )
    #
    # print(result)



