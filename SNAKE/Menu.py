import pygame_menu
import pygame


class Menu:
    def __init__(self, game):
        def newGame():
            game.PLAY_MODE = "Player"
            # adding params to main game loop the game loop returns the new crossed over population
            game.game_loop(True, turns_in_simulation, 0, gen)

        def train_ai():
            game.PLAY_MODE = "AI"

        def best_ai():
            game.PLAY_MODE = "Show_best"

        pygame.init()

        self.menu = pygame_menu.Menu('SNAKE with Neural Networks', game.SCREEN_WIDTH, game.SCREEN_HEIGHT,
                                     theme=pygame_menu.themes.THEME_ORANGE)
        self.menu.add.button("New Game", newGame)
        self.menu.add.button("Train AI", train_ai)
        self.menu.add.button("Best AI", best_ai)
        self.menu.add.button('Exit', pygame_menu.events.EXIT)

        # -----------------------------------------------------------------------------

        pygame.display.set_caption("snake")

        pygame.font.init()  # you have to call this at the start,
        # if you want to use this module.
        self.my_font = pygame.font.SysFont('Comic Sans MS', 15)

        self.enable(game)

    def enable(self, game):
        self.menu.mainloop(game.display)
