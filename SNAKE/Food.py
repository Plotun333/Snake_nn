# import libraries
import pygame
# import files
from SNAKE.GameInfo import GameInfo


class Food:
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y

        # red
        self.color = (255, 0, 0)

        self.width = 10
        self.height = 10

        # helps keep track of the food in a list
        self.index = 1

    def draw(self, game):
        pygame.draw.rect(game.display, self.color, (self.x, self.y, self.width, self.height))
