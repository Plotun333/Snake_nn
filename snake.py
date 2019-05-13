# imports

import pygame
import pygameMenu
import sys
import os
import random
import math

from pygameMenu.locals import *

# show display in the middle of the screen
os.environ['SDL_VIDEO_CENTERED'] = '1'

# frame rate + delay after every frame
FPS = 12
delay = 50


class GameInfo(object):
    """
    Game info is a class with all of the global information about the game
    like the display the Score...
    """

    def __init__(self):
        self.screen_width = 600
        self.screen_height = 600
        self.Score = 0
        self.display = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        self.DEATH = False


class Snake(GameInfo):
    def __init__(self, x=300, y=300):
        super().__init__()
        # default x,y
        self.x = int(x)
        self.y = int(y)
        self.body_width = 10
        self.body_height = 10
        self.color = (0, 255, 0)
        self.speed = 10
        self.body = [[self.x, self.y]]
        self.dir = 'left'
        self.pause = False

    def draw(self):
        # moving the body + drawing it
        index = 0
        moveto = []
        for element in self.body:

            if index == 0:
                moveto.append([self.body[0][0], self.body[0][1]])
                if self.dir == 'left':
                    self.body[0][0] -= self.speed

                elif self.dir == 'right':
                    self.body[0][0] += self.speed

                elif self.dir == 'up':
                    self.body[0][1] -= self.speed

                elif self.dir == 'down':
                    self.body[0][1] += self.speed
            else:
                moveto.append([element[0], element[1]])
                element = moveto[len(moveto) - 2]
                self.body[index] = element

            pygame.draw.rect(self.display, self.color, (element[0], element[1], self.body_width, self.body_height))

            index += 1

    def move(self, menu):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            keys = pygame.key.get_pressed()

            for _ in keys:
                if keys[pygame.K_LEFT] and self.dir != 'right':

                    self.dir = 'left'

                elif keys[pygame.K_RIGHT] and self.dir != 'left':

                    self.dir = 'right'

                elif keys[pygame.K_UP] and self.dir != 'down':

                    self.dir = 'up'

                elif keys[pygame.K_DOWN] and self.dir != 'up':

                    self.dir = 'down'

                elif keys[pygame.K_ESCAPE]:
                    menu.enable()

    def eat(self, x, y):
        if x == self.body[0][0] and y == self.body[0][1]:
            if self.dir == 'left':
                x, y = self.body[len(self.body) - 1]
                self.body.append([x + self.speed, y])
            elif self.dir == 'right':
                x, y = self.body[len(self.body) - 1]
                self.body.append([x - self.speed, y])
            elif self.dir == 'up':
                x, y = self.body[len(self.body) - 1]
                self.body.append([x, y + self.speed])
            elif self.dir == 'down':
                x, y = self.body[len(self.body) - 1]
                self.body.append([x, y - self.speed])

            return True

    def hit(self):
        x, y = self.body[0]

        index = 0
        for element in self.body:
            if index != 0:
                if x == element[0] and y == element[1]:
                    return True
            if x < 0 or x >= 600 or y >= 600 or y < 0:
                return True
            index += 1
        return False

    # Input for AI

    def food_angle(self, x, y):
        del_x = self.body[0][0] - x
        del_y = self.body[0][1] - y
        degree = math.degrees(math.atan2(del_x, del_y))
        if 0 > degree:
            return (360 + degree) / 360
        else:
            return degree / 360

    def wall_dist_left(self):

        return (self.body[0][0] + 10)/610

    def wall_dist_right(self):

        return (self.screen_height - self.body[0][0])/600

    def wall_dist_up(self):

        return (self.body[0][1] + 10)/610

    def wall_dist_down(self):

        return (self.screen_height - self.body[0][1])/600


class Food(GameInfo):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.color = (255, 0, 0)
        self.width = 10
        self.height = 10

    def draw(self):
        pygame.draw.rect(self.display, self.color, (self.x, self.y, self.width, self.height))


class Game(object):
    """
    The main game class
    """
    def __init__(self):
        self.game = GameInfo()
        self.snake = Snake()
        self.food = Food(random.randint(1, 59) * self.snake.speed, random.randint(1, 59) * self.snake.speed)

    def main_menu_background(self):
        """
        Background color of the main menu, on this function user can plot
        images, play sounds, etc.
        """
        self.game.display.fill((40, 0, 40))

    def game_loop(self, show=True):
        pygame.init()
        white = (255, 255, 255)

        # -----------------------------------------------------------------------------
        # Main menu, pauses execution of the application

        def main_menu_background():
            """
            Background color of the main menu, on this function user can plot
            images, play sounds, etc.
            """
            game.game.display.fill((216, 216, 216))

        def train_ai():
            pass

        menu = pygameMenu.Menu(self.game.display,
                               bgfun=main_menu_background,
                               enabled=False,
                               font=pygameMenu.fonts.FONT_NEVIS,
                               menu_alpha=90,
                               onclose=PYGAME_MENU_CLOSE,
                               title='Main Menu',
                               title_offsety=5,
                               window_height=int(self.game.screen_height),
                               window_width=int(self.game.screen_width)
                               )

        menu.add_option("New Game", train_ai)
        menu.add_option("Train AI", train_ai)
        menu.add_option("Player vs AI", train_ai)
        menu.add_option('Exit', PYGAME_MENU_EXIT)

        # -----------------------------------------------------------------------------

        pygame.display.set_caption("snake")

        pygame.font.init()  # you have to call this at the start,
        # if you want to use this module.
        my_font = pygame.font.SysFont('Comic Sans MS', 15)
        if not show:
            pygame.display.iconify()

        while True:
            events = pygame.event.get()

            text_surface = my_font.render('Score:  ' + str(self.game.Score), False, (255, 0, 0))
            self.game.display.fill(white)
            pygame.time.delay(delay)
            self.game.clock.tick(FPS)
            self.game.display.blit(text_surface, (10, 10))
            self.snake.draw()
            self.food.draw()
            self.snake.move(menu)
            if self.snake.eat(self.food.x, self.food.y):
                self.game.Score += 1
                self.food = Food(random.randint(1, 59) * self.snake.speed, random.randint(1, 59) * self.snake.speed)
                self.game.display.fill(white)

            if self.snake.hit():
                self.snake.body = [[300, 300]]
                self.game.Score = 0
                self.game.DEATH = True
                self.snake.dir = 'left'
            menu.mainloop(events)
            pygame.display.flip()


game = Game()

game.game_loop()
