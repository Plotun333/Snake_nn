# import libraries
import pygame

import sys
import random
from lib_nn.nn import NeuralNetwork

# import Files
from GameInfo import GameInfo
from Snake import Snake
from Food import Food
from Menu import Menu



class Game:
    """
    The main game class
    """

    def __init__(self, population=None):
        self.PLAY_MODE = None
        self.DEATH = True
        self.SCREEN_WIDTH = 800
        self.SCREEN_HEIGHT = 400
        self.Score = 0
        self.display = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        if population is None:  # normal game

            self.snake = Snake()
            self.food = Food(random.randint(1, 39) * self.snake.SPEED, random.randint(1, 39) * self.snake.SPEED)

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
                    Food(random.randint(1, 39) * self.snake.SPEED, random.randint(1, 39) * self.snake.SPEED))

        self.population = population
        self.menu = Menu(self)

    def game_loop(self, show=True, max_turns=300, delay=50, gen=None):

        Play_normal = "None"
        pygame.init()
        white = (255, 255, 255)
        if self.population is None:
            AI = False
        else:
            AI = True

        # -----------------------------------------------------------------------------
        # Main menu, pauses execution of the application

        menu = Menu(self)

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

            self.display.fill(white)
            pygame.time.delay(delay)
            self.clock.tick(FPS)

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
                            menu.enable(self)

                remove_s = []
                remove_f = []
                remove_nn = []
                index = 0

                self.display.fill((0, 0, 0))
                for nn in self.population:

                    self.all_food[index].draw(self)
                    self.all_snake[index].ai(nn, self.all_food[index], menu, self)
                    self.all_snake[index].draw(self)

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
                        self.all_snake[index].Fitness -= max_turns
                        remove_s.append(self.all_snake[index])
                        remove_f.append(self.all_food[index])
                        remove_nn.append(nn)

                    if self.all_snake[index].eat(self.all_food[index].x, self.all_food[index].y):
                        self.Score += 1
                        self.all_food[index] = Food(random.randint(1, 39) * self.snake.SPEED,
                                                    random.randint(1, 39) * self.snake.SPEED)
                        self.scores[index] += 1
                        self.display.fill((0, 0, 0))
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

                text_surface3 = my_font.render('Loading: ' + str(turns) + ' / ' + str(max_turns), False, (255, 0, 0))
                text_surface2 = my_font.render('Generation: ' + str(gen), False, (255, 0, 0))
                text_surface = my_font.render('Best global score: ' + str(max(self.scores)), False, (255, 0, 0))
                self.display.blit(text_surface3, (500, 200))
                self.display.blit(text_surface2, (500, 175))
                self.display.blit(text_surface, (500, 150))
                pygame.draw.line(self.display, (255, 255, 255), (self.SCREEN_HEIGHT, 0),
                                 (self.SCREEN_HEIGHT, self.SCREEN_HEIGHT))
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
                self.display.fill((0, 0, 0))

                text_surface = my_font.render('Score: ' + str(self.Score), False, (255, 0, 0))
                self.display.blit(text_surface, (10, 10))
                self.food.draw(self)
                self.snake.move(menu)
                self.snake.draw(self)

                pygame.draw.line(self.display, (255, 255, 255), (self.SCREEN_HEIGHT, 0),
                                 (self.SCREEN_HEIGHT, self.SCREEN_HEIGHT))

                if self.snake.eat(self.food.x, self.food.y):
                    self.Score += 1
                    self.food = Food(random.randint(1, 39) * self.snake.SPEED, random.randint(1, 39) * self.snake.SPEED)
                    self.display.fill((0, 0, 0))

                if self.snake.hit():
                    return None

                pygame.display.flip()

            if Play_normal != "None":
                return Play_normal

    def simulate(self, nn, fitness="unknown"):
        global Play_mode
        Play_mode = "None"
        pygame.init()
        white = (255, 255, 255)
        self.snake = Snake()
        self.food = Food(random.randint(1, 39) * self.snake.SPEED, random.randint(1, 39) * self.snake.SPEED)
        simulate_nn = nn

        # -----------------------------------------------------------------------------
        # Main menu, pauses execution of the application

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
                        self.menu.enable(self)

            events = pygame.event.get()
            self.display.fill(white)
            all_fit = 0
            if not fitness == "unknown":
                for fit in fitness:
                    all_fit += fit
                average = all_fit / len(fitness)
                text_surface = self.menu.my_font.render('Best Fitness: ' + str(fitness[0]),
                                                        False, (100, 200, 24))
                text_surface2 = self.menu.my_font.render("Average Fitness: " + str(average), False, (100, 200, 24))
                self.display.blit(text_surface, (500, 200))
                self.display.blit(text_surface2, (500, 175))

            pygame.time.delay(delay)
            self.clock.tick(fps)
            self.display.fill((0, 0, 0))
            self.food.draw(self)
            self.snake.ai(simulate_nn, self.food, self.menu, self)
            self.snake.draw(self)

            if self.snake.hit():
                return None

            if self.snake.eat(self.food.x, self.food.y):
                self.Score += 1
                self.food = Food(random.randint(1, 39) * self.snake.SPEED, random.randint(1, 39) * self.snake.SPEED)
                self.food.index += 1
                self.display.fill((0, 0, 0))

            # self.menu.mainloop(events)

            pygame.display.flip()

            if Play_mode != "None":
                return Play_mode
