
# import libraries
import math
import pygame
import sys

# import files
from SNAKE.GameInfo import GameInfo


class Snake:

    def __init__(self, x=200, y=200):  # default position is in the middle of the "snake screen"
        super().__init__()
        # default x,y
        self.x = int(x)
        self.y = int(y)

        self.BODY_WIDTH = 10
        self.BODY_HEIGHT = 10
        # the snake is green
        self.COLOR = (0, 255, 0)

        self.SPEED = 10
        # the head of the snake
        self.body = [[self.x, self.y]]
        # the snake starts the game moving left
        self.dir = 'left'

        self.pause = False
        # AI
        self.Fitness = 0
        self.food_dist = 0

    def draw(self, game):
        # moving the body + drawing it
        index = 0
        moveto = []
        for element in self.body:

            if index == 0:  # move the head
                moveto.append([self.body[0][0], self.body[0][1]])
                if self.dir == 'left':
                    self.body[0][0] -= self.SPEED

                elif self.dir == 'right':
                    self.body[0][0] += self.SPEED

                elif self.dir == 'up':
                    self.body[0][1] -= self.SPEED

                elif self.dir == 'down':
                    self.body[0][1] += self.SPEED
            else:  # move the rest of the body to the position were the previous body was
                moveto.append([element[0], element[1]])
                element = moveto[len(moveto) - 2]
                self.body[index] = element

            pygame.draw.rect(game.display, self.COLOR, (element[0], element[1], self.BODY_WIDTH, self.BODY_HEIGHT))

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

    def ai(self, nn, food, menu, game):  # the ai move function
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            keys = pygame.key.get_pressed()

            for _ in keys:
                if keys[pygame.K_ESCAPE]:
                    menu.enable()

        # the neural network inputs
        input_nn = [
            # eight wall inputs
            self.wall_dist_up(),
            self.wall_dist_up_right(game),
            self.wall_dist_right(game),
            self.wall_dist_right_down(game),
            self.wall_dist_down(game),
            self.wall_dist_down_left(game),
            self.wall_dist_left(),
            self.wall_dist_left_up(),

            # eight body inputs
            self.body_dist_up(),
            self.body_dist_up_right(),
            self.body_dist_down(),
            self.body_dist_right_down(),
            self.body_dist_right(),
            self.body_dist_down_left(),
            self.body_dist_left(),
            self.body_dist_left_up(),

            # eight food distance inputs
            self.food_dist_up(food),
            self.food_dist_up_right(food),
            self.food_dist_right(food),
            self.food_dist_right_down(food),
            self.food_dist_down(food),
            self.food_dist_down_left(food),
            self.food_dist_left(food),
            self.food_dist_left_up(food)
        ]

        # add the inputs to the neural network (feed forward function)

        output = nn.feed_forward(input_nn)

        # get the biggest output witch will be the ai's choice
        dir_index = output.index(max(output))

        # neural network will give four outputs: up or right or left or down
        # left
        if dir_index == 0:
            if not self.dir == "right":
                self.dir = "left"

        # right
        elif dir_index == 1:
            if not self.dir == "left":
                self.dir = "right"

        # up
        elif dir_index == 2:
            if not self.dir == "down":
                self.dir = "up"

        # down
        elif dir_index == 3:
            if not self.dir == "up":
                self.dir = "down"

    def eat(self, x, y):
        if x == self.body[0][0] and y == self.body[0][1]:
            # if the snake eats food his body will grow by one 10 by 10 square but to render this animation correctly
            # we have to write account form witch direction he eats the food

            if self.dir == 'left':
                x, y = self.body[len(self.body) - 1]
                self.body.append([x + self.SPEED, y])
            elif self.dir == 'right':
                x, y = self.body[len(self.body) - 1]
                self.body.append([x - self.SPEED, y])
            elif self.dir == 'up':
                x, y = self.body[len(self.body) - 1]
                self.body.append([x, y + self.SPEED])
            elif self.dir == 'down':
                x, y = self.body[len(self.body) - 1]
                self.body.append([x, y - self.SPEED])

            return True

    def hit(self):  # check if the snake hits its tail or the walls
        x, y = self.body[0]

        index = 0
        for element in self.body:
            if index != 0:
                if x == element[0] and y == element[1]:
                    return True
            if x < 0 or x >= 400 or y >= 400 or y < 0:
                return True
            index += 1
        return False

    # Input for AI

    def food_angle(self, food):
        del_x = self.body[0][0] - food.x
        del_y = self.body[0][1] - food.y
        degree = math.degrees(math.atan2(del_x, del_y))
        if 0 > degree:
            return (360 + degree) / 360
        else:
            return degree / 360

    # the canvas is wide and high 410 pixels  (corner to corner 841)

    """
    these function allow the snake to see they all return a value from 0-1 one is if the snake is close to an 
    element. zero is if we either doesn't see the element or the element is very far from him 
    
    """

    # WALL
    def wall_dist_left(self):
        return 1 - ((self.body[0][0] + 10) / 410)

    def wall_dist_right(self, game):
        return 1 - ((game.SCREEN_WIDTH - self.body[0][0]) / 400)

    def wall_dist_up(self):
        return 1 - ((self.body[0][1] + 10) / 410)

    def wall_dist_down(self, game):
        return 1 - ((game.SCREEN_HEIGHT - self.body[0][1]) / 400)

    def wall_dist_up_right(self, game):
        return 1 - ((1 / 2) ** (self.wall_dist_up() ** 2 + self.wall_dist_right(game) ** 2))

    def wall_dist_right_down(self, game):
        return 1 - ((1 / 2) ** (self.wall_dist_right(game) ** 2 + self.wall_dist_down(game) ** 2))

    def wall_dist_down_left(self, game):
        return 1 - ((1 / 2) ** (self.wall_dist_down(game) ** 2 + self.wall_dist_left() ** 2))

    def wall_dist_left_up(self):
        return 1 - ((1 / 2) ** (self.wall_dist_left() ** 2 + self.wall_dist_up() ** 2))

    # FOOD
    def distance_from_food(self, food):  # not used
        return (math.hypot(food.x - self.body[0][0], food.y - self.body[0][1])) / 566

    def food_dist_up_right(self, food):
        x, y = self.body[0]
        if food.x - x == y - food.y and food.x > x:

            return 1 - ((math.hypot(food.x - x, food.y - y)) / 566)
        else:
            return 0

    def food_dist_right_down(self, food):
        x, y = self.body[0]
        if food.x - food.y == x - y and food.x > x:

            return 1 - ((math.hypot(food.x - x, food.y - y)) / 566)
        else:
            return 0

    def food_dist_down_left(self, food):
        x, y = self.body[0]
        if food.x - x == y - food.y and food.x < x:

            return 1 - ((math.hypot(food.x - x, food.y - y)) / 566)
        else:
            return 0

    def food_dist_left_up(self, food):
        x, y = self.body[0]
        if - food.y + food.x == - y + x and food.x < x:

            return 1 - ((math.hypot(food.x - x, food.y - y)) / 566)
        else:
            return 0

    def food_dist_right(self, food):
        x, y = self.body[0]
        if food.y == y and food.x > x:
            return 1 - ((food.x - x) / 400)
        else:
            return 0

    def food_dist_left(self, food):
        x, y = self.body[0]
        if food.y == y and food.x < x:
            return 1 - ((x - food.x) / 400)
        else:
            return 0

    def food_dist_up(self, food):
        x, y = self.body[0]
        if food.x == x and food.y < y:
            return 1 - ((y - food.y) / 400)
        else:
            return 0

    def food_dist_down(self, food):
        x, y = self.body[0]
        if food.x == x and food.y > y:
            return 1 - ((food.y - y) / 400)
        else:
            return 0

    # BODY
    def body_dist_left(self):
        x, y = self.body[0]
        index = 0

        for element in self.body:
            if index != 0:
                if y == element[1] and x > element[0]:
                    return 1 - ((x - element[0]) / 400)

            index += 1
        return 0

    def body_dist_right(self):
        x, y = self.body[0]
        index = 0

        for element in self.body:
            if index != 0:
                if y == element[1] and x < element[0]:
                    return 1 - ((element[0] - x) / 400)

            index += 1
        return 0

    def body_dist_up(self):
        x, y = self.body[0]
        index = 1

        for element in self.body:
            if index != 0:
                if x == element[0] and y > element[1]:
                    return 1 - ((y - element[1]) / 400)

            index += 1
        return 0

    def body_dist_down(self):
        x, y = self.body[0]
        index = 0

        for element in self.body:
            if index != 0:
                if x == element[0] and y < element[1]:
                    return 1 - ((element[1] - y) / 400)

            index += 1
        return 0

    def body_dist_up_right(self):
        x, y = self.body[0]
        index = 0

        for element in self.body:
            if index != 0:
                if element[0] - x == y - element[1] and element[0] > x:
                    return 1 - ((math.hypot(x - element[0], y - element[1])) / 566)

            index += 1
        return 0

    def body_dist_right_down(self):
        x, y = self.body[0]
        index = 0

        for element in self.body:
            if index != 0:
                if element[0] - element[1] == x - y and element[0] > x:
                    return 1 - ((math.hypot(x - element[0], y - element[1])) / 566)

            index += 1
        return 0

    def body_dist_down_left(self):
        x, y = self.body[0]
        index = 0

        for element in self.body:
            if index != 0:
                if element[0] - x == y - element[1] and element[0] < x:
                    return 1 - ((math.hypot(x - element[0], y - element[1])) / 566)

            index += 1
        return 0

    def body_dist_left_up(self):
        x, y = self.body[0]
        index = 0

        for element in self.body:
            if index != 0:
                if - element[1] + element[0] == - y + x and element[0] < x:
                    return 1 - ((math.hypot(x - element[0], y - element[1])) / 566)

            index += 1
        return 0
