import pygame
import sys
import random

FPS = 12
delay = 50


class Game(object):
    def __init__(self):
        self.screen_width = 600
        self.screen_height = 600
        self.Score = 0
        self.display = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()


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
        self.dir = 'left'

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
            if x < 0 or x > 600 or y > 600 or y < 0:
                return True
            index += 1
        return False


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


def main():
    pygame.init()
    white = (255, 255, 255)
    green = (0, 255, 0)
    game = Game()
    pygame.display.set_caption("snake")
    snake = Snake()
    food = Food(random.randint(1, 59) * 10, random.randint(1, 59) * 10)
    pygame.font.init()  # you have to call this at the start,
    # if you want to use this module.
    my_font = pygame.font.SysFont('Comic Sans MS', 15)

    while True:

        text_surface = my_font.render('Score:  ' + str(game.Score), False, (255, 0, 0))
        if snake.eat(food.x, food.y):
            game.Score += 1
            food = Food(random.randint(1, 59) * 10, random.randint(1, 59) * 10)
        pygame.time.delay(delay)
        game.clock.tick(FPS)
        game.display.fill(white)
        game.display.blit(text_surface, (10, 10))
        snake.draw()
        food.draw()
        snake.move()
        if snake.hit():
            print("you lost")
            # x, y = snake.body[0]
            # snake.body = [[x, y]]

        pygame.display.update()
