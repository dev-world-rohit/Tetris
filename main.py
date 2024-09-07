import pygame
from pygame.locals import *

pygame.init()


class Game:
    def __init__(self):
        self.border_width = 2
        self.outline = 5
        self.padding = 20
        self.screen_size = [32 * 10 + 200 + self.padding * 3, 32 * 20 + self.padding * 2]
        self.screen = pygame.display.set_mode(self.screen_size)

        self.game_surface = pygame.Surface([32 * 10, 32 * 20])
        self.next_surface = pygame.Surface(
            [self.screen_size[0] - (self.game_surface.get_width() + self.padding * 3), self.screen_size[1] // 3])
        self.score_surface = pygame.Surface(
            [self.next_surface.get_width(), self.screen_size[1] - self.next_surface.get_height() - self.padding * 3])

        self.clock = pygame.time.Clock()
        self.fps = 30

        self.block_patterns = [
            [[1, 0, 0],
             [1, 1, 1]],
            [[1, 1, 1],
             [1, 0, 0]],
            [[1, 1],
             [1, 1]],
            [[0, 1, 1],
             [1, 1, 0]],
            [[1, 1, 0],
             [0, 1, 1]],
            [[1, 1, 1, 1]],
            [[1, 1, 1],
             [0, 1, 0]]
        ]

        self.run = True

    def draw_bordered_surface(self, surface, position):
        surface.fill((255, 255, 255))
        pygame.draw.rect(self.screen, (255, 255, 255),
                         [position[0] - self.border_width, position[1] - self.border_width,
                          surface.get_width() + self.border_width * 2,
                          surface.get_height() + self.border_width * 2], 2)
        self.screen.blit(surface, position)

    def game_loop(self):
        while self.run:
            # Filling the surfaces---------------------------#
            self.screen.fill((0, 0, 0))
            self.draw_bordered_surface(self.game_surface, [self.padding, self.padding])
            self.draw_bordered_surface(self.next_surface,
                                       [self.game_surface.get_width() + 2 * self.padding, self.padding])
            self.draw_bordered_surface(self.score_surface,
                                       [self.game_surface.get_width() + 2 * self.padding,
                                        self.next_surface.get_height() + 2 * self.padding])

            self.game_surface.fill((0, 0, 0))
            self.next_surface.fill((0, 0, 0))
            self.score_surface.fill((0, 0, 0))

            # Drawing the lines on the game screen--------------------------#
            for i in range(10):
                for j in range(20):
                    pygame.draw.rect(self.game_surface, (255, 255, 255),
                                     (i * 32, j * 32, self.game_surface.get_width(), self.game_surface.get_height()), 1)

            # Key binding-----------------------------#
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.run = False

            # Surfaces blit to the main screen-------------------------#
            self.screen.blit(self.game_surface, [self.padding, self.padding])
            self.screen.blit(self.next_surface,
                             [self.game_surface.get_width() + 2 * self.padding, self.padding])
            self.screen.blit(self.score_surface, [self.game_surface.get_width() + 2 * self.padding,
                                                  self.next_surface.get_height() + 2 * self.padding])
            pygame.display.update()
            self.clock.tick(self.fps)

        pygame.quit()


game = Game()
game.game_loop()
