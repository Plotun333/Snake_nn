# import libraries
import os

# import files
from lib_nn.nn import NeuralNetwork
from SNAKE.Game import Game

# show display in the middle of the screen
os.environ['SDL_VIDEO_CENTERED'] = '1'

# initial population
# params
population_num = 1000  # number of snakes in population
input_nn = 24  # number of inputs
hidden = [18]  # number of hidden layers
output = 3  # number of outputs forward / left / right
turns_in_simulation = 300  # number of turns in a simulation

population = NeuralNetwork.initial_population(population_num, input_nn, hidden, output)  # creating initial population
gen = 1  # the simulation starts at generation 1

if __name__ == '__main__':
    while True:
        # creating game if population is a list of neural networks the game will be a simulation
        game = Game(population)

        # adding params to main game loop the game loop returns the new crossed over population
        population = game.game_loop(True, turns_in_simulation, 0, gen)

        # if the user changes the game in the menu the game loop will return: Player or AI
        if population == "Player":
            population = None
        elif population == "AI":
            population = NeuralNetwork.initial_population(population_num, input_nn, hidden, output)
        elif population is not None:
            # population is a tuple with the new crossed over population and all of the sorted fitness from best to
            # worst
            print("Gen: ", gen)
            all_fit = 0
            for fit in population[1]:
                all_fit += fit
            print("Average Fitness: ", all_fit / len(population[1]))
            print("Best Fitness:", population[1][0])
            print('\n')
            # every five simulation the best player will be simulated alone
            if gen % 5 == 0:
                game.simulate(population[0], population[1])

            for nn in population[0]:  # mutate
                nn.mutate(0.01)
            population = population[0]

        gen += 1
