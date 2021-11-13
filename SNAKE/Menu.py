import pygame_menu
import pygame
import pickle
from lib_nn.nn import NeuralNetwork
from Game import Game

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400


class Menu:
    def __init__(self, turnsInSimulation, population_num, input_nn, hidden, output, gen):
        self.turnsInSimulation = turnsInSimulation
        self.population_num = population_num
        self.input_nn = input_nn
        self.hidden = hidden
        self.output = output
        self.gen = gen

        self.game = None

        pygame.init()
        self.display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.menu = pygame_menu.Menu('SNAKE with Neural Networks', SCREEN_WIDTH, SCREEN_HEIGHT,
                                     theme=pygame_menu.themes.THEME_ORANGE)
        self.menu.add.button("Single Player", self.newGame)
        self.menu.add.button("Train AI", self.train_ai)
        self.menu.add.button("Best AI", self.best_ai)
        self.menu.add.button('Exit', pygame_menu.events.EXIT)

        # -----------------------------------------------------------------------------

        pygame.display.set_caption("snake")
        #
        pygame.font.init()  # you have to call this at the start,

    def enable(self):
        self.menu.mainloop(self.display)

    def newGame(self):
        self.game = Game(self.gen, self, None)
        self.game.PLAY_MODE = "Player"

        # adding params to main game loop the game loop returns the new crossed over population
        self.game.game_loop(True, self.turnsInSimulation, 0, self.gen)

    def train_ai(self):
        population = NeuralNetwork.initial_population(self.population_num, self.input_nn, self.hidden, self.output)
        self.game = Game(self.gen, self, population)

        self.game.PLAY_MODE = "AI"

        # adding params to main game loop the game loop returns the new crossed over population
        self.game.game_loop(True, self.turnsInSimulation, 0, self.gen)

    def best_ai(self):
        self.game = Game(self.gen, self, None)

        self.game.PLAY_MODE = "Show_best"

        with open('best_nn_data.pkl', 'rb') as input_file:
            best_nn = pickle.load(input_file)
            print(best_nn.Fitness)
        self.game.simulate(best_nn)
        # adding params to main game loop the game loop returns the new crossed over population
        # game.game_loop(True, turnsInSimulation, 0, gen)
