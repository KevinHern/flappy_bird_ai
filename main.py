# AI
from flappy_bird_ai.flappy_bird.games.flappy_bird_ai import FlappyBirdAI
from flappy_bird_ai.flappy_bird.artificial_intelligence.neat_setup import NeatSetup


if __name__ == '__main__':
    # Setting up Game
    game = FlappyBirdAI(
        number_pipes=50
    )

    # Setting up NEAT Algorithm
    neatSetup = NeatSetup(
        simulation=game.simulation,
        max_generations=2,
        neat_checkpoint=11,
        load_checkpoint_number=10
    )

    # Run
    neatSetup.start_simulation()
