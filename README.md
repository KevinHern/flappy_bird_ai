# Flappy Bird AI

This is a project that consisted of trying to recreate the famous game of Flappy Bird but with the twist of adding Artificial Intelligence and let it learn how to play it until it mastered said game.

## Pitch

### Why Neural Networks?

Flappy bird is a game that works within the continuous world; that means, there are variables that are a real number. Neural Networks are pretty good at condensing a set of parameters into a single action: flap or no flap.

The birds have the following 4 variables:
- **Bird Y position** or known as **Height**
- **X distance** from **closest Pipe**
- **Height** of the **closest Top Pipe**
- **Height** of the **closest Bottom Pipe**

All of them are real numbers

### Why Genetic Algorithms?

Based on Charles Darwin's Evolution Theory, only the strongest survive and pass on their genes - we can apply the same idea with artificial intelligence!

The program will create different birds with different Neural Network parameters; no bird is identical.
Then, all the birds (called 'generation') are subjected to run in the game and the ones that perform the best, will be used as a model to create the next generation of birds by passing down their parameters and suffer mutations along the way.

### Why NEAT?

NEAT is the hybrid between Neural Networks and Genetic Algorithms mashed together.
Each new generation, the Neural Network parameters can be modified by making the net more complex.

# Run

If you wish to test the artificial intelligence, feel free to use **GitPod.io** to run the project.

[![Open in Gitpod](https://gitpod.io/button/open-in-gitpod.svg)](https://gitpod.io/#https://github.com/KevinHern/flappy_bird_ai)

Also, if you want to visualize how the neural network evolves as generations go on, make sure to constantly check the **growth** directory (it will automatically create itself). 