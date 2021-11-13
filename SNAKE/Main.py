# import libraries
import os
from lib_nn.nn import NeuralNetwork
from Menu import Menu
from Game import Game

# show display in the middle of the screen
os.environ['SDL_VIDEO_CENTERED'] = '1'

# initial population
# params
population_num = 2000  # number of snakes in population
input_nn = 24  # number of inputs
hidden = [18]  # number of hidden layers
output = 4  # number of outputs: up / left / right / down
turnsInSimulation = 30  # number of turns in a simulation

population = NeuralNetwork.initial_population(population_num, input_nn, hidden, output)  # creating initial population
gen = 1  # the simulation starts at generation 1

# all x => generations in graph
x = []
y = []

if __name__ == '__main__':

        menu = Menu(turnsInSimulation, population_num, input_nn, hidden, output, gen)
        menu.enable()
