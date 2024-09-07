import random
import pygame
from pygame.locals import *

pygame.init()

class Game:
    def __init__(self):
        self.border_width = 2
        self.outline = 5
        self.padding = 20
        self.block_size = 32
        self.screen_size = [self.block_size * 10 + 200 + self.padding * 3, self.block_size * 20 + self.padding * 2]
        self.screen = pygame.display.set_mode(self.screen_size)

        self.game_surface = pygame.Surface([self.block_size * 10, self.block_size * 20])
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

        self.board = [[0 for _ in range(10)] for _ in range(20)]
        self.block = None
        self.next_block = random.choice(self.block_patterns)  # Initialize next block
        self.block_pos = [4, 0]  # Block starting position (4th column, 0th row)

        self.gravity = 0.1  # Speed of gravity
        self.gravity_timer = 0  # Timer to control block fall speed

        self.prepare_block()

        self.run = True

    def draw_bordered_surface(self, surface, position):
        surface.fill((255, 255, 255))
        pygame.draw.rect(self.screen, (255, 255, 255),
                         [position[0] - self.border_width, position[1] - self.border_width,
                          surface.get_width() + self.border_width * 2,
                          surface.get_height() + self.border_width * 2], 2)
        self.screen.blit(surface, position)

    def prepare_block(self):
        self.block = self.next_block
        self.next_block = random.choice(self.block_patterns)
        self.block_pos = [4, 4]  # Reset block position to the top of the screen

    def display_next_block(self):
        pos_x = (self.next_surface.get_width() - (len(self.next_block[0]) * self.block_size)) // 2
        pos_y = (self.next_surface.get_height() - (len(self.next_block) * self.block_size)) // 2

        for i in range(len(self.next_block)):
            for j in range(len(self.next_block[i])):
                if self.next_block[i][j] != 0:
                    pygame.draw.rect(self.next_surface, (255, 255, 255), (
                        pos_x + self.block_size * j + 1, pos_y + self.block_size * i + 1, self.block_size - 2,
                        self.block_size - 2))

    def display_block(self):
        for i in range(len(self.block)):
            for j in range(len(self.block[i])):
                if self.block[i][j] != 0:
                    x = self.block_pos[0] + j
                    y = self.block_pos[1] + i
                    if 0 <= x < 10 and 0 <= y < 20:  # Ensure block is within bounds
                        pygame.draw.rect(self.game_surface, (255, 0, 0), (
                            x * self.block_size + 1, y * self.block_size + 1, self.block_size - 2,
                            self.block_size - 2))

    # def update_block_position(self):
    #     # Gravity effect
    #     self.gravity_timer += self.gravity
    #     if self.gravity_timer >= 1:  # Move block down when the timer reaches 1
    #         self.block_pos[1] += 1
    #         self.gravity_timer = 0
    #
    #     # Check if block reached the bottom of the screen or hit another block
    #     if self.block_pos[1] + len(self.block) >= 20 or self.check_collision():
    #         self.place_block()
    #         self.prepare_block()
    #
    # def check_collision(self):
    #     for i in range(len(self.block)):
    #         for j in range(len(self.block[i])):
    #             if self.block[i][j] != 0:
    #                 x = self.block_pos[0] + j
    #                 y = self.block_pos[1] + i
    #                 if y >= 20 or self.board[y][x] != 0:
    #                     return True
    #     return False
    #
    # def place_block(self):
    #     for i in range(len(self.block)):
    #         for j in range(len(self.block[i])):
    #             if self.block[i][j] != 0:
    #                 x = self.block_pos[0] + j
    #                 y = self.block_pos[1] + i
    #                 if 0 <= x < 10 and 0 <= y < 20:
    #                     self.board[y][x] = self.block[i][j]

    def draw_board(self):
        for i in range(10):
            for j in range(20):
                if self.board[j][i] != 0:
                    pygame.draw.rect(self.game_surface, (255, 0, 255), (
                        i * self.block_size + 1, j * self.block_size + 1, self.block_size - 2,
                        self.block_size - 2))

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
                                     (i * self.block_size, j * self.block_size, self.block_size, self.block_size), 1)

            # Show the next block on the next_block_screen-----------------------#
            self.display_next_block()

            # Display the current block and update its position
            # self.update_block_position()
            self.display_block()

            # Draw the placed blocks on the board
            self.draw_board()

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
