# imports

import pygame
import pygameMenu
import sys
import os
import random
import math

from pygameMenu.locals import *
from lib_nn.nn import NeuralNetwork

# show display in the middle of the screen
os.environ['SDL_VIDEO_CENTERED'] = '1'


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
        # AI
        self.Fitness = 0
        self.food_dist = None

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

    def ai(self, nn, food, menu):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            keys = pygame.key.get_pressed()

            for _ in keys:
                if keys[pygame.K_ESCAPE]:
                    menu.enable()

        input = [self.wall_dist_up(),
                 self.wall_dist_down(),
                 self.wall_dist_right(),
                 self.wall_dist_left(),
                 self.food_angle(food.x, food.y)]

        output = nn.feed_forward(input)

        index = 0
        current_val = -1
        for val in output:
            if val > current_val:
                dir_index = index
            current_val = val
            index += 1
        # neural network will give three outputs if forward or right or right
        # foward doesn't change anything in the current game state

        if dir_index == 1:
            if self.dir == "up":
                self.dir = "right"
            elif self.dir == "right":
                self.dir = "down"
            elif self.dir == "down":
                self.dir = "right"
            elif self.dir == "left":
                self.dir = "up"

        elif dir_index == 2:
            if self.dir == "up":
                self.dir = "left"
            elif self.dir == "right":
                self.dir = "up"
            elif self.dir == "down":
                self.dir = "left"
            elif self.dir == "left":
                self.dir = "down"

    def fitness(self, food):
        dist = math.hypot(self.body[0][0] - food.x, self.body[0][1] - food.y)
        if self.food_dist is not None:
            if dist < self.food_dist:
                self.Fitness += 0.001
            else:
                self.Fitness -= 0.001
        self.food_dist = dist

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

        return (self.body[0][0] + 10) / 610

    def wall_dist_right(self):

        return (self.screen_height - self.body[0][0]) / 600

    def wall_dist_up(self):

        return (self.body[0][1] + 10) / 610

    def wall_dist_down(self):

        return (self.screen_height - self.body[0][1]) / 600


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

    def __init__(self, population=None):
        self.game = GameInfo()
        if population is None:
            self.snake = Snake()
            self.food = Food(random.randint(1, 59) * self.snake.speed, random.randint(1, 59) * self.snake.speed)

        else:
            self.all_food = []
            self.snake = Snake()
            self.all_snake = []

            for _ in population:
                self.all_snake.append(Snake())
                self.all_food.append(
                    Food(random.randint(1, 59) * self.snake.speed, random.randint(1, 59) * self.snake.speed))
        # self.food = Food(random.randint(1, 59) * self.snake.speed, random.randint(1, 59) * self.snake.speed)
        self.population = population

    def main_menu_background(self):
        """
        Background color of the main menu, on this function user can plot
        images, play sounds, etc.
        """
        self.game.display.fill((40, 0, 40))

    def game_loop(self, show=True, max_turns=300, delay=50, gen=None):
        pygame.init()
        white = (255, 255, 255)
        if self.population is None:
            AI = False
        else:
            AI = True

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

        All_fitness = []
        next_puplation = []
        turns = 0

        # frame rate + delay after every frame
        FPS = 12
        delay = delay
        while True:
            events = pygame.event.get()

            self.game.display.fill(white)
            pygame.time.delay(delay)
            self.game.clock.tick(FPS)

            if AI:
                # UI
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()

                    keys = pygame.key.get_pressed()

                    for _ in keys:

                        if keys[pygame.K_ESCAPE]:
                            menu.enable()

                remove_s = []
                remove_f = []
                remove_nn = []
                index = 0
                for nn in self.population:

                    self.all_food[index].draw()
                    self.all_snake[index].ai(nn, self.all_food[index], menu)
                    self.all_snake[index].draw()
                    self.all_snake[index].fitness(self.all_food[index])
                    if turns >= max_turns:
                        remove_s = []
                        remove_f = []
                        remove_nn = []
                        for snake in self.all_snake:
                            remove_s.append(snake)
                        for food in self.all_food:
                            remove_f.append(food)
                        for n in self.population:
                            remove_nn.append(n)
                        break

                    if self.all_snake[index].hit():
                        self.game.DEATH = True
                        self.all_snake[index].Fitness -= 100
                        remove_s.append(self.all_snake[index])
                        remove_f.append(self.all_food[index])
                        remove_nn.append(nn)

                    if self.all_snake[index].eat(self.all_food[index].x, self.all_food[index].y):
                        self.game.Score += 1
                        self.all_food[index] = Food(random.randint(1, 59) * self.snake.speed,
                                                    random.randint(1, 59) * self.snake.speed)
                        self.game.display.fill(white)
                        self.all_snake[index].Fitness += 50

                    index += 1
                for r in remove_s:
                    # print(r.Fitness)
                    All_fitness.append(r.Fitness)
                    self.all_snake.remove(r)
                for r in remove_f:
                    self.all_food.remove(r)
                for r in remove_nn:
                    next_puplation.append(r)
                    self.population.remove(r)
                menu.mainloop(events)

                self.game.display.fill(white)
                text_surface2 = my_font.render('Loading: ' + str(turns) + ' / ' + str(max_turns), False, (255, 0, 0))
                text_surface = my_font.render('Generation: ' + str(gen), False, (255, 0, 0))
                self.game.display.blit(text_surface2, (230, 250))
                self.game.display.blit(text_surface, (230, 200))
                pygame.display.flip()
                turns += 1

                # showing the best player and mixing gen poll
                if len(self.all_snake) == 0:

                    # sorting from biggest to smallest
                    All_fitness_sorted = []
                    next_puplation_sorted = []
                    while All_fitness:
                        # find index of maximum item
                        max_index = All_fitness.index(max(All_fitness))

                        # remove item with pop() and append to sorted list
                        next_puplation_sorted.append(next_puplation[max_index])
                        next_puplation.remove(next_puplation[max_index])
                        All_fitness_sorted.append(All_fitness[max_index])
                        All_fitness.remove(All_fitness[max_index])

                    # breading the best and killing the worst
                    all_percent = []
                    current_percent = 100
                    one_percent = 100 / len(next_puplation_sorted)
                    for _ in next_puplation_sorted:
                        all_percent.append(current_percent / 100)
                        current_percent -= one_percent

                    index = 0
                    expected = len(next_puplation_sorted)

                    remove = []
                    for percent in all_percent:
                        r = random.randint(0, 10000) / 10000

                        if r > percent:
                            remove.append(next_puplation_sorted[index])
                        index += 1
                    for r in remove:
                        next_puplation_sorted.remove(r)
                    # mutating and creating new population

                    current_population = len(next_puplation_sorted)

                    add = []
                    for _ in range(expected - current_population):
                        r = random.randint(0, current_population - 1)
                        new_nn = next_puplation_sorted[r].copy()
                        new_nn.mutate(0.1)

                        add.append(new_nn)

                    for nn in add:
                        next_puplation_sorted.append(nn)

                    print(All_fitness_sorted)
                    return next_puplation_sorted

            else:
                text_surface = my_font.render('Score:  ' + str(self.game.Score), False, (255, 0, 0))
                self.game.display.blit(text_surface, (10, 10))
                self.food.draw()
                self.snake.move(menu)
                self.snake.draw()

                if self.snake.eat(self.food.x, self.food.y):
                    self.game.Score += 1
                    self.food = Food(random.randint(1, 59) * self.snake.speed, random.randint(1, 59) * self.snake.speed)
                    self.game.display.fill(white)

                if self.snake.hit():
                    return None

                menu.mainloop(events)
                pygame.display.flip()

    def simulate(self, nn):
        pygame.init()
        white = (255, 255, 255)
        self.snake = Snake()
        self.food = Food(random.randint(1, 59) * self.snake.speed,
                         random.randint(1, 59) * self.snake.speed)

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

        # frame rate + delay after every frame
        FPS = 12
        delay = 50

        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                keys = pygame.key.get_pressed()

                for _ in keys:
                    if keys[pygame.K_SPACE]:
                        return None

                    if keys[pygame.K_ESCAPE]:
                        menu.enable()

            events = pygame.event.get()

            text_surface = my_font.render('Fitness:  ', False, (255, 0, 0))
            self.game.display.blit(text_surface, (10, 10))
            self.game.display.fill(white)
            pygame.time.delay(delay)
            self.game.clock.tick(FPS)

            self.food.draw()
            self.snake.ai(nn, self.food, menu)
            self.snake.draw()

            if self.snake.hit():
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()

                        keys = pygame.key.get_pressed()

                        for _ in keys:
                            if keys[pygame.K_SPACE]:
                                return None

            if self.snake.eat(self.food.x, self.food.y):
                self.game.Score += 1
                self.food = Food(random.randint(1, 59) * self.snake.speed,
                                 random.randint(1, 59) * self.snake.speed)
                self.game.display.fill(white)

            menu.mainloop(events)

            pygame.display.flip()


# initial population

population = NeuralNetwork.initial_population(100, 5, [5], 3)
gen = 1
while True:
    game = Game(population)

    population = game.game_loop(True, 300, 0, gen)
    if population is not None:
        game.simulate(population[0])
    gen+=1