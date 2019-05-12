import snake
import tflearn
import numpy
import random
import math

snake.main()

class NeuralNetwork(object):
    def __init__(self,  initial_games = 1000, test_games = 100, goal_steps = 100, lr = 1e-2, filename = 'snake_nn.tflearn'):
        self.initial_games = initial_games
        self.test_games = 100
        self.goal_steps = 100
        self.lr = 1e-2
        self.filename = filename

    def initial_population(self):
        training_data = []
        for _ in range(self.initial_games):
            game = snake.Game()
            _, _, snake, _ = game.start()
            prev_observation = self.generate_observation(snake)
            for _ in range(self.goal_steps):
                action, game_action = self.generate_action(snake)
                done, _, snake, _ = game.step(game_action)
                if done:
                    training_data.append([self.add_action_to_observation(prev_observation, action), 0])
                    break
                else:
                    training_data.append([self.add_action_to_observation(prev_observation, action), 1])
                    prev_observation = self.generate_observation(snake)
        print(len(training_data))
        return training_data



