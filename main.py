import snake
import tflearn
import numpy
import random
import math

#game = snake.Game()
#game.game_loop()

class NeuralNetwork(object):
    def __init__(self,  initial_games = 100, test_games = 100, goal_steps = 100, lr = 1e-2, filename = 'snake_nn.tflearn'):
        self.initial_games = initial_games
        self.test_games = 100
        self.goal_steps = 100
        self.lr = 1e-2
        self.filename = filename
        self.training_data = []

    def initial_population(self):

        for _ in range(self.initial_games):
            print("here")

            prev_observation = self.generate_observation()
            for _ in range(self.goal_steps):
                print("here2")
                action, game_action = self.generate_action()
                done = snake.Game.game.DEATH
                if done:
                    self.training_data.append([(prev_observation, action), 0])
                    break
                else:
                    self.training_data.append([(prev_observation, action), 1])
                    prev_observation = self.generate_observation()
        print(len(self.training_data))


    def generate_observation(self,snake):
        fruit_angle = snake.Game.snake.fruit_angle
        top_wall = game.snake.top_wall
        bottom_wall = snake.Game.snake.bottom_wall
        left_wall = snake.Game.snake.left_wall
        right_wall = snake.Game.snake.right_wall

        return [fruit_angle, top_wall, bottom_wall, right_wall, left_wall]


    def generate_action(self):
        action = random.randint(0,2) - 1
        if snake.Game.snake.dir == "up":
            if action == -1:
                dir = "left"
            elif action == 1:
                dir = "right"
            elif action == 0:
                dir = "up"

        elif snake.Game.snake.dir == "down":
            if action == -1:
                dir = "right"
            elif action == 1:
                dir = "left"
            elif action == 0:
                dir = "down"

        elif snake.Game.snake.dir == "right":
            if action == -1:
                dir = "up"
            elif action == 1:
                dir = "down"
            elif action == 0:
                dir = "right"


        elif snake.Game.snake.dir == "left":
            if action == -1:
                dir = "down"
            elif action == 1:
                dir = "up"
            elif action == 0:
                dir = "left"

        snake.Game.snake.dir = dir

        return action, dir


