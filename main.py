# AI
from simulation.flappy_bird_ai import FlappyBirdAI
from simulation.models.bird_agent import BirdAgent
from neat_utility import NeatSetup


if __name__ == '__main__':
    # Setting up Game
    '''
        YOU CAN MODIFY THE NUMBER OF PIPES FOR THE GAMES!!!
    '''
    game = FlappyBirdAI(
        number_pipes=50
    )

    # Setting up NEAT Algorithm
    '''
        YOU CAN MODIFY THE FOLLOWING PARAMETERS:
        - max_generations: The total number of max generations
            that the game will run
        - load_checkpoint_number: You can start the game with
            a fresh generations or start from a checkpoint
            * None: Start from a fresh generation
            * Integer: Either 10 or 49
    '''

    neatSetup = NeatSetup(
        max_generations=50,
        neat_checkpoint_breakpoint=10,
        file_prefix="flappy_bird",
        simulation_file=__file__,
        is_feedforward_network=True,
        inputs_name=["Bird's Y position", "Closest Pipe's farthest corner's X position", "Top pipe's height", "Bottom pipe's height"],
        outputs_name=["Flap"],

        load_checkpoint_number=None,
        # load_checkpoint_number=10
        config_file=None,
        simulation=game.simulation,

        logging_function=BirdAgent.log_stats
    )

    # Run
    neatSetup.run_simulation()
