# utils
from os.path import join, dirname

# AI
import neat


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

    # Run for up to 50 generations.
    winner = generation.run(simulation, max_generations)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))
