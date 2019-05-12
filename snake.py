import pygame
import sys
import random
import math

FPS = 12
delay = 50


class Game(object):
    def __init__(self):
        self.screen_width = 600
        self.screen_height = 600
        self.Score = 0
        self.display = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        self.DEATH = False


class Snake(Game):
    def __init__(self):
        super().__init__()
        self.x = int(300)
        self.y = int(300)
        self.body_width = 10
        self.body_height = 10
        self.color = (0, 255, 0)
        self.speed = 10
        self.body = [[self.x, self.y]]
        self.dir = 'none '

    def draw(self):
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

    def move(self):
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
                    pygame.quit()
                    sys.exit()

    def eat(self, x, y):
        if x == self.body[0][0] and y == self.body[0][1]:
            if self.dir == 'left':
                x, y = self.body[len(self.body) - 1]
                self.body.append([x + self.speed, y])
            elif self.dir == 'right':
                x, y = self.body[len(self.body) - 1]
                self.body.append([x + self.speed, y])
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


class Food(Game):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.color = (255, 0, 0)
        self.width = 10
        self.height = 10

    def draw(self):
        pygame.draw.rect(self.display, self.color, (self.x, self.y, self.width, self.height))


def main(show=True):
    pygame.init()
    white = (255, 255, 255)
    game = Game()

    pygame.display.set_caption("snake")
    snake = Snake()
    food = Food(random.randint(1, 59) * snake.speed, random.randint(1, 59) * snake.speed)
    pygame.font.init()  # you have to call this at the start,
    # if you want to use this module.
    my_font = pygame.font.SysFont('Comic Sans MS', 15)
    if not show:
        pygame.display.iconify()

    while True:

        text_surface = my_font.render('Score:  ' + str(game.Score), False, (255, 0, 0))
        game.display.fill(white)
        pygame.time.delay(delay)
        game.clock.tick(FPS)
        game.display.blit(text_surface, (10, 10))
        snake.draw()
        food.draw()
        snake.move()
        if snake.eat(food.x, food.y):
            game.Score += 1
            food = Food(random.randint(1, 59) * snake.speed, random.randint(1, 59) * snake.speed)
            game.display.fill(white)

        if snake.hit():
            snake.body = [[300, 300]]
            game.Score = 0
            game.DEATH = True
            snake.dir = 'none'
        pygame.display.update()
