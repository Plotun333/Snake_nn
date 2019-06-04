# import libraries
import pygame
import pygameMenu
from pygameMenu.locals import *
import sys
import random
from lib_nn.nn import NeuralNetwork

# import Files
from SNAKE.GameInfo import GameInfo
from SNAKE.snake import Snake
from SNAKE.food import Food


class Game(object):
    """
    The main game class
    """

    def __init__(self, population=None):
        self.game = GameInfo()

        if population is None:  # normal game

            self.snake = Snake()
            self.food = Food(random.randint(1, 39) * self.snake.speed, random.randint(1, 39) * self.snake.speed)

        else:
            self.all_food_pos = []

            self.all_food = []
            self.snake = Snake()
            self.all_snake = []
            self.scores = []  # Ai scorers

            for _ in range(len(population)):
                self.all_snake.append(Snake())
                self.scores.append(0)  # append a score
                self.all_food.append(
                    Food(random.randint(1, 39) * self.snake.speed, random.randint(1, 39) * self.snake.speed))

        self.population = population

    def game_loop(self, show=True, max_turns=300, delay=50, gen=None):
        global Play_normal
        Play_normal = "None"
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
            # Nothing

        def play():
            global Play_normal
            Play_normal = "Player"

        def train_ai():
            global Play_normal
            Play_normal = "AI"

        def best_ai():
            global Play_normal
            Play_normal = "Show_best"

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

        menu.add_option("New Game", play)
        menu.add_option("Train AI", train_ai)
        menu.add_option("Best AI", best_ai)
        menu.add_option('Exit', PYGAME_MENU_EXIT)

        # -----------------------------------------------------------------------------

        pygame.display.set_caption("snake")

        pygame.font.init()  # you have to call this at the start,
        # if you want to use this module.
        my_font = pygame.font.SysFont('Comic Sans MS', 15)
        if not show:
            pygame.display.iconify()

        All_fitness = []
        next_population = []
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
                FPS = 120
                delay = 0
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

                self.game.display.fill((0, 0, 0))
                for nn in self.population:

                    self.all_food[index].draw()
                    self.all_snake[index].ai(nn, self.all_food[index], menu)
                    self.all_snake[index].draw()

                    self.all_snake[index].Fitness += 2

                    self.all_snake[index].food_dist = self.all_snake[index].distance_from_food(self.all_food[index])
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
                        self.all_snake[index].Fitness -= max_turns
                        remove_s.append(self.all_snake[index])
                        remove_f.append(self.all_food[index])
                        remove_nn.append(nn)

                    if self.all_snake[index].eat(self.all_food[index].x, self.all_food[index].y):
                        self.game.Score += 1
                        self.all_food[index] = Food(random.randint(1, 39) * self.snake.speed,
                                                    random.randint(1, 39) * self.snake.speed)
                        self.scores[index] += 1
                        self.game.display.fill((0, 0, 0))
                        self.all_snake[index].Fitness += max_turns

                    index += 1
                for r in remove_s:
                    # print(r.Fitness)
                    All_fitness.append(r.Fitness)
                    self.all_snake.remove(r)
                for r in remove_f:
                    self.all_food.remove(r)
                for r in remove_nn:
                    next_population.append(r)
                    self.population.remove(r)
                menu.mainloop(events)

                text_surface3 = my_font.render('Loading: ' + str(turns) + ' / ' + str(max_turns), False, (255, 0, 0))
                text_surface2 = my_font.render('Generation: ' + str(gen), False, (255, 0, 0))
                text_surface = my_font.render('Best global score: ' + str(max(self.scores)), False, (255, 0, 0))
                self.game.display.blit(text_surface3, (500, 200))
                self.game.display.blit(text_surface2, (500, 175))
                self.game.display.blit(text_surface, (500, 150))
                pygame.draw.line(self.game.display, (255, 255, 255), (self.game.screen_height, 0),
                                 (self.game.screen_height, self.game.screen_height))
                pygame.display.flip()
                turns += 1

                # showing the best player and mixing gen poll
                if len(self.all_snake) == 0:

                    # sorting from biggest to smallest
                    All_fitness_sorted = []
                    next_population_sorted = []
                    while All_fitness:
                        # find index of maximum item
                        max_index = All_fitness.index(max(All_fitness))

                        # remove item with pop() and append to sorted list
                        next_population_sorted.append(next_population[max_index])
                        next_population.remove(next_population[max_index])
                        All_fitness_sorted.append(All_fitness[max_index])
                        All_fitness.remove(All_fitness[max_index])

                    # breading the best and killing the worst
                    all_percent = []
                    current_percent = 100
                    one_percent = 100 / len(next_population_sorted)
                    for _ in next_population_sorted:
                        all_percent.append(current_percent / 100)
                        current_percent -= one_percent

                    index = 0
                    expected = len(next_population_sorted)

                    remove = []
                    for percent in all_percent:
                        r = random.randint(0, 10000) / 10000

                        if r > percent:
                            remove.append(next_population_sorted[index])
                        index += 1

                    for r in remove:
                        next_population_sorted.remove(r)
                    # mutating and creating new population
                    current_population = NeuralNetwork.cross_over(next_population_sorted, expected)

                    return current_population, All_fitness_sorted

            else:
                self.game.display.fill((0, 0, 0))

                text_surface = my_font.render('Score: ' + str(self.game.Score), False, (255, 0, 0))
                self.game.display.blit(text_surface, (10, 10))
                self.food.draw()
                self.snake.move(menu)
                self.snake.draw()

                pygame.draw.line(self.game.display, (255, 255, 255), (self.game.screen_height, 0),
                                 (self.game.screen_height, self.game.screen_height))

                if self.snake.eat(self.food.x, self.food.y):
                    self.game.Score += 1
                    self.food = Food(random.randint(1, 39) * self.snake.speed, random.randint(1, 39) * self.snake.speed)
                    self.game.display.fill((0, 0, 0))

                if self.snake.hit():
                    return None

                menu.mainloop(events)
                pygame.display.flip()

            if Play_normal != "None":
                return Play_normal

    def simulate(self, nn, fitness="unknown"):
        global Play_normal
        Play_normal = "None"
        pygame.init()
        white = (255, 255, 255)
        self.snake = Snake()
        self.food = Food(random.randint(1, 39) * self.snake.speed, random.randint(1, 39) * self.snake.speed)
        simulate_nn = nn

        # -----------------------------------------------------------------------------
        # Main menu, pauses execution of the application

        def main_menu_background():
            """
            Background color of the main menu, on this function user can plot
            images, play sounds, etc.
            """
            # Nothing

        def play():
            global Play_normal
            Play_normal = "Player"

        def train_ai():
            global Play_normal
            Play_normal = "AI"

        def best_ai():
            global Play_normal
            Play_normal = "Show_best"

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

        menu.add_option("New Game", play)
        menu.add_option("Train AI", train_ai)
        menu.add_option("Best AI", best_ai)
        menu.add_option('Exit', PYGAME_MENU_EXIT)

        # -----------------------------------------------------------------------------

        pygame.display.set_caption("snake")

        pygame.font.init()  # you have to call this at the start,
        # if you want to use this module.
        my_font = pygame.font.SysFont('Comic Sans MS', 15)

        # frame rate + delay after every frame
        fps = 36
        delay = 0
        while True:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                keys = pygame.key.get_pressed()

                for _ in keys:
                    if keys[pygame.K_ESCAPE]:
                        menu.enable()

            events = pygame.event.get()
            self.game.display.fill(white)
            all_fit = 0
            if not fitness == "unknown":
                for fit in fitness:
                    all_fit += fit
                average = all_fit / len(fitness)
                text_surface = my_font.render('Best Fitness: ' + str(fitness[0]),
                                              False, (100, 200, 24))
                text_surface2 = my_font.render("Average Fitness: " + str(average), False, (100, 200, 24))
                self.game.display.blit(text_surface, (500, 200))
                self.game.display.blit(text_surface2, (500, 175))

            pygame.time.delay(delay)
            self.game.clock.tick(fps)
            self.game.display.fill((0, 0, 0))
            self.food.draw()
            self.snake.ai(simulate_nn, self.food, menu)
            self.snake.draw()

            if self.snake.hit():
                return None

            if self.snake.eat(self.food.x, self.food.y):
                self.game.Score += 1
                self.food = Food(random.randint(1, 39) * self.snake.speed, random.randint(1, 39) * self.snake.speed)
                self.food.index += 1
                self.game.display.fill((0, 0, 0))

            menu.mainloop(events)

            pygame.display.flip()

            if Play_normal != "None":
                return Play_normal
