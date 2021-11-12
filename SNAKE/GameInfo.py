import pygame


class GameInfo:
    """
    Game info is a class with all of the global information about the game
    like the display the Score...
    """

    def __init__(self):
        self.screen_width = 800
        self.screen_height = 400
        self.Score = 0
        self.display = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
