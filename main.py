# AI
from flappy_bird.games.flappy_bird_ai import FlappyBirdAI
from flappy_bird.artificial_intelligence.neat_setup import NeatSetup


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
        simulation=game.simulation,
        max_generations=50,
        neat_checkpoint=11,
        load_checkpoint_number=None,
        #load_checkpoint_number=10
    )

    # Run
    neatSetup.start_simulation()
