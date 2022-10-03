# AI
import neat

# utils
import shutil
from os.path import join, dirname, exists
from os import mkdir, listdir
import logging
from datetime import datetime


class NeatSetup:
    CONFIG_PATH = join(dirname(dirname(__file__)), 'artificial_intelligence', 'config-feedforward.txt')
    LOG_PATH = join(dirname(dirname(__file__)), 'logs')
    CHECKPOINT_PATH = join(dirname(dirname(__file__)), 'checkpoints')
    NEAT_CHECKPOINT_FILE_PREFIX = "neat-checkpoint"
    GAMES_DIRECTORY = join(dirname(dirname(__file__)), 'games')
    MAIN_PY_DIRECTORY = dirname(dirname(dirname(__file__)))

    def __init__(self, simulation, max_generations, neat_checkpoint, load_checkpoint_number=None):
        # Initializing parameters for simulations
        self.simulation = simulation
        self.max_generations = max_generations
        self.neat_checkpoint = neat_checkpoint
        self.load_checkpoint_number = load_checkpoint_number

        # Parsing configuration file
        self.config_file = neat.config.Config(
            neat.DefaultGenome, neat.DefaultReproduction,
            neat.DefaultSpeciesSet, neat.DefaultStagnation,
            NeatSetup.CONFIG_PATH
        )

        # Create checkpoint directory if it doesn't exist
        if not exists(NeatSetup.CHECKPOINT_PATH):
            mkdir(NeatSetup.CHECKPOINT_PATH)

        # Create logs directory if it doesn't exist
        if not exists(NeatSetup.LOG_PATH):
            mkdir(NeatSetup.LOG_PATH)

        # Setting up logger
        today_date = datetime.today().strftime('%Y_%m_%d-%H_%M')
        logging.basicConfig(
            filename=join(NeatSetup.LOG_PATH, 'training_log_neat_{}.log'.format(today_date)),
            filemode='w',
            level=logging.INFO,
            format='\n%(asctime)s-%(levelname)s> %(message)s',
            datefmt='%d-%b-%y %H:%M:%S'
        )

    @staticmethod
    def _move_checkpoints():
        # Moving checkpoint files
        for file in listdir(NeatSetup.MAIN_PY_DIRECTORY):
            if file.startswith(NeatSetup.NEAT_CHECKPOINT_FILE_PREFIX):
                shutil.move(
                    src=join(NeatSetup.MAIN_PY_DIRECTORY, file),
                    dst=join(NeatSetup.CHECKPOINT_PATH, file)
                )

    def _neat_setup(self):
        # Creating population
        generation = neat.Population(self.config_file)

        # Adding statistics and logging capabilities
        generation.add_reporter(neat.StdOutReporter(True))
        generation.add_reporter(neat.StatisticsReporter())
        generation.add_reporter(neat.Checkpointer(self.neat_checkpoint))

        # Run for up to max_generations generations.
        winner = generation.run(self.simulation, self.max_generations)

        # Show stats of the best Genome
        print('\nBest genome:\n{!s}'.format(winner))

        # Moving checkpoints
        NeatSetup._move_checkpoints()

    def _restore_population_checkpoint(self):
        # Obtaining the path of the checkpoint
        checkpoint_path = join(
            NeatSetup.CHECKPOINT_PATH,
            '{}-{}'.format(NeatSetup.NEAT_CHECKPOINT_FILE_PREFIX, self.load_checkpoint_number)
        )

        # Creating population
        generation = neat.Checkpointer.restore_checkpoint(checkpoint_path)

        # Adding statistics and logging capabilities
        generation.add_reporter(neat.StdOutReporter(True))
        generation.add_reporter(neat.StatisticsReporter())
        generation.add_reporter(neat.Checkpointer(self.neat_checkpoint))

        # Run for up to max_generations generations.
        winner = generation.run(self.simulation, self.max_generations)

        # Show stats of the best Genome
        print('\nBest genome:\n{!s}'.format(winner))

        # Moving checkpoints
        NeatSetup._move_checkpoints()

        # # Save Neural Network
        # local_dir = dirname(dirname(__file__))
        # filename = join(local_dir, 'artificial_intelligence', 'neural_network.json')
        #
        # convert_genome_to_json(
        #     filename=filename,
        #     genome=winner,
        #     config=config,
        #     inputs_name=[
        #         "Bird Y Position",
        #         "X position of the farthest corner",
        #         "Top pipe's height",
        #         "Bottom pipe's height",
        #     ],
        #     outputs_name=["Flap"]
        # )

    def start_simulation(self):
        if self.load_checkpoint_number is None:
            self._neat_setup()
        else:
            self._restore_population_checkpoint()

    @staticmethod
    def log_stats(winner_genome):
        # Creating message to log
        message = "\n---END OF GENERATION {}---\n".format(winner_genome)
        message += "Fittest Score: {}\n".format(winner_genome.genome.fitness)
        message += "Fittest Pipes passed: {}\n".format(winner_genome.pipes_passed)
        message += "Track {:.2f}% completed".format(100 * winner_genome.pipes_passed / winner_genome.total_pipes)

        # Logging
        logging.info(
            msg=message
        )
