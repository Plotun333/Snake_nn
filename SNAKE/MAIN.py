# import libraries
import os
import pickle
import matplotlib.pyplot as plt

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
output = 4  # number of outputs: up / left / right / down
turns_in_simulation = 300  # number of turns in a simulation

population = NeuralNetwork.initial_population(population_num, input_nn, hidden, output)  # creating initial population
gen = 1  # the simulation starts at generation 1

# all x => generations in graph
x = []
y = []

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

        elif population == "Show_best":
            with open('best_nn_data.pkl', 'rb') as input_file:
                best_nn = pickle.load(input_file)
                print(best_nn.Fitness)

            break

        elif population is not None:
            # average fitness
            all_fit = 0
            for fit in population[1]:
                all_fit += fit
            average_fitness = all_fit / len(population[1])
            # save the best snake into a file using pickle
            # checking if the snake is really the best snake ever created
            population[0][0].Fitness = population[1][0]
            try:
                with open('best_nn_data.pkl', 'rb') as input_file:
                    best_nn = pickle.load(input_file)
                if best_nn.Fitness < population[0][0].Fitness:
                    best_nn = population[0][0]
                    with open('best_nn_data.pkl', 'wb') as output:
                        print("adding best snake")
                        pickle.dump(best_nn, output, pickle.HIGHEST_PROTOCOL)

            except FileNotFoundError:
                print("New file created")
                with open('best_nn_data.pkl', 'wb') as output:
                    best_nn = population[0][0]
                    pickle.dump(best_nn, output, pickle.HIGHEST_PROTOCOL)

            x.append(gen)
            y.append(average_fitness)

            if gen % 5 == 0:
                plt.plot(x, y, label='Fitness')

                plt.xlabel('Average Fitness')
                plt.ylabel('Generations')

                plt.title("Fitness")

                plt.legend()

                plt.show()

            # population is a tuple with the new crossed over population and all of the sorted fitness from best to
            # worst
            print("Gen: ", gen)

            print("Average Fitness: ", average_fitness)
            print("Best Fitness:", population[1][0])
            print('\n')

            # every five simulation the best player will be simulated alone
            # if gen % 5 == 0:
            # game.simulate(population[0][0], population[1])

            for nn in population[0]:  # mutate
                nn.mutate(0.01)
            population = population[0]

            gen += 1
