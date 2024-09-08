import webbrowser
import pygame
import random
from data.scripts.text import font
from data.scripts.image_functions import import_image
from pygame.locals import *

pygame.init()
pygame.mixer.init()


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

        self.home_bg = import_image('background.png')

        self.start_button = import_image('start_button.png', (0, 0, 0))
        self.start_button_hover = import_image('start_button_hover.png', (0, 0, 0))
        self.exit_button = import_image('exit.png', (0, 0, 0))
        self.exit_button_hover = import_image('exit_hover.png', (0, 0, 0))
        self.like = import_image('like.png', (0, 0, 0))
        self.like_button_hover = import_image('like_hover.png', (0, 0, 0))
        self.button_bg = import_image('button_bg.png', (0, 0, 0), 20)

        self.buttons = {
            "start": [self.start_button, self.start_button_hover],
            "exit": [self.exit_button, self.exit_button_hover],
            "like": [self.like, self.like_button_hover]
        }

        # Importing sounds---------------------------------#
        pygame.mixer.music.load('data/sounds/background_music.mp3')
        pygame.mixer.music.play(loops=-1)

        self.press_sound = pygame.mixer.Sound('data/sounds/pressed.mp3')

        self.text = font('small_font.png', (255, 255, 255), 3)
        self.score_text = font('small_font.png', (255, 255, 255), 5)
        self.title_text = font('small_font.png', (255, 0, 0), 10)

        self.clock = pygame.time.Clock()
        self.fps = 30

        self.block_patterns = [
            [[2, 0, 0],
             [1, 1, 1]],
            [[2, 1, 1],
             [1, 0, 0]],
            [[2, 2],
             [1, 1]],
            [[0, 2, 1],
             [1, 1, 0]],
            [[1, 2, 0],
             [0, 1, 1]],
            [[1, 1, 1, 1]],
            [[1, 2, 1],
             [0, 1, 0]]
        ]

        self.colors = [
            (255, 0, 0),
            (0, 255, 0),
            (0, 0, 255),
            (255, 255, 0),
            (255, 0, 255),
            (0, 255, 255),
            (127, 127, 127)
        ]

        self.board = [[0 for _ in range(10)] for _ in range(20)]
        self.block = None
        self.next_block = [random.choice(self.block_patterns), random.choice(self.colors)]
        self.block_pos = [4, -2]

        self.gravity = 0.1
        self.gravity_timer = 0

        # self.prepare_block()

        self.score = 0
        self.run = True

    def draw_bordered_surface(self, surface, position):
        surface.fill((255, 255, 255))
        pygame.draw.rect(self.screen, (255, 255, 255),
                         [position[0] - self.border_width, position[1] - self.border_width,
                          surface.get_width() + self.border_width * 2,
                          surface.get_height() + self.border_width * 2], 2)
        self.screen.blit(surface, position)

    def prepare_block(self):
        self.press_sound.play()
        self.block = self.next_block
        self.next_block = [random.choice(self.block_patterns), random.choice(self.colors)]
        self.block_pos = [4, -2]

    def display_next_block(self):
        pos_x = (self.next_surface.get_width() - (len(self.next_block[0][0]) * self.block_size)) // 2
        pos_y = (self.next_surface.get_height() - (len(self.next_block[0]) * self.block_size)) // 2

        for i in range(len(self.next_block[0])):
            for j in range(len(self.next_block[0][i])):
                if self.next_block[0][i][j] != 0:
                    pygame.draw.rect(self.next_surface, self.next_block[1], (
                        pos_x + self.block_size * j + 1, pos_y + self.block_size * i + 1, self.block_size - 2,
                        self.block_size - 2))

    def display_block(self):
        for i in range(len(self.block[0])):
            for j in range(len(self.block[0][i])):
                if self.block[0][i][j] != 0:
                    x = self.block_pos[0] + j
                    y = self.block_pos[1] + i
                    if 0 <= x < 10 and 0 <= y < 20:
                        pygame.draw.rect(self.game_surface, self.block[1], (
                            x * self.block_size + 1, y * self.block_size + 1, self.block_size - 2,
                            self.block_size - 2))

    def update_block_position(self):
        self.gravity_timer += self.gravity
        if self.gravity_timer >= 1:
            self.block_pos[1] += 1
            if self.check_collision():
                self.block_pos[1] -= 1
                self.lock_block()
                self.prepare_block()
            self.gravity_timer = 0

    def lock_block(self):
        for i in range(len(self.block[0])):
            for j in range(len(self.block[0][i])):
                if self.block[0][i][j] != 0:
                    x = self.block_pos[0] + j
                    y = self.block_pos[1] + i
                    if y >= 0:
                        self.board[y][x] = self.block[1]
        cleared_rows = self.clear_rows()
        if cleared_rows > 0:
            self.update_score(cleared_rows)
        self.check_game_over()

    def check_side_collision(self, dx):
        for i in range(len(self.block[0])):
            for j in range(len(self.block[0][i])):
                if self.block[0][i][j] != 0:
                    x = self.block_pos[0] + j + dx
                    y = self.block_pos[1] + i
                    if x < 0 or x >= 10 or (y >= 0 and self.board[y][x] != 0):
                        return True
        return False

    def check_collision(self):
        for i in range(len(self.block[0])):
            for j in range(len(self.block[0][i])):
                if self.block[0][i][j] != 0:
                    x = self.block_pos[0] + j
                    y = self.block_pos[1] + i

                    if y >= 20 or (y >= 0 and self.board[y][x] != 0):
                        return True
        return False

    def check_game_over(self):
        for j in range(len(self.block[0])):
            for i in range(len(self.block[0][j])):
                if self.block[0][j][i] != 0 and self.block_pos[1] + j < 0:
                    self.run = False
                    self.display_game_over()

    def rotate_block(self):
        original_block = self.block[0]
        self.block[0] = [list(row) for row in zip(*self.block[0][::-1])]

        if self.check_collision() or self.out_of_bounds():
            self.block[0] = original_block

    def out_of_bounds(self):
        for i in range(len(self.block[0])):
            for j in range(len(self.block[0][i])):
                if self.block[0][i][j] != 0:
                    x = self.block_pos[0] + j
                    y = self.block_pos[1] + i
                    if x < 0 or x >= 10 or y >= 20:
                        return True
        return False

    def draw_board(self):

        for i in range(10):
            for j in range(20):
                if self.board[j][i] != 0:
                    pygame.draw.rect(self.game_surface, self.board[j][i], (
                        i * self.block_size + 1, j * self.block_size + 1, self.block_size - 2,
                        self.block_size - 2))

    def clear_rows(self):
        full_rows = [i for i in range(20) if all(self.board[i])]
        for row in full_rows:
            del self.board[row]
            self.board.insert(0, [0 for _ in range(10)])
        return len(full_rows)

    def update_score(self, rows_cleared):
        points = {1: 100, 2: 300, 3: 500, 4: 800}
        self.score += points.get(rows_cleared, 0)
        print("Score:", self.score)

    def update_level(self):
        self.level = self.score // 1000
        self.gravity = max(0.05, 1 - self.level * 0.1)

    def display_home_screen(self):
        while True:
            self.screen.fill((0, 0, 0))
            self.screen.blit(self.home_bg, (0, 0))
            mouse_pos = pygame.mouse.get_pos()
            pos = [(self.screen_size[0] - self.start_button.get_width()) // 2, 200]
            offset = 0
            for button in self.buttons:
                button_rect = pygame.Rect(pos[0], pos[1] + offset, self.buttons[button][0].get_width(),
                                          self.buttons[button][0].get_height())
                if button_rect.collidepoint(mouse_pos):
                    self.screen.blit(self.button_bg, button_rect.topleft)
                    self.screen.blit(self.buttons[button][1], button_rect.topleft)
                    if pygame.mouse.get_pressed()[0]:
                        self.press_sound.play()
                        if button == "start":
                            self.game_loop()
                        elif button == "exit":
                            pygame.quit()
                            return
                        else:
                            webbrowser.open('www.linkedin.com/in/rohit-dewaliya-a12801280')
                else:
                    self.screen.blit(self.buttons[button][0], button_rect.topleft)

                offset += 80

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    return

            pygame.display.update()
            self.clock.tick(self.fps)

    def display_game_over(self):
        run = True
        while run:
            # Filling the surfaces---------------------------#
            self.screen.fill((0, 0, 0))
            self.title_text.display_fonts(self.screen, "Game Over!", [130, 250])
            self.text.display_fonts(self.screen, "Your Score is " + str(self.score), [190, 350])
            self.text.display_fonts(self.screen, "Press r to continue...", [170, 400])

            # Key binding-----------------------------#
            for event in pygame.event.get():
                if event.type == QUIT:
                    run = False

                if event.type == KEYDOWN:
                    if event.key == K_r:
                        self.press_sound.play()
                        run = False
                        self.display_home_screen()

            pygame.display.update()
            self.clock.tick(self.fps)

        pygame.quit()

    def game_loop(self):
        self.prepare_block()
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

            self.title_text.display_fonts(self.score_surface, "Score", [25, 10])
            self.score_text.display_fonts(self.score_surface, str(self.score), [(self.score_surface.get_width() - len(str(self.score) * 15)) // 2, 100])

            # Drawing the lines on the game screen--------------------------#
            for i in range(10):
                for j in range(20):
                    pygame.draw.rect(self.game_surface, (255, 255, 255),
                                     (i * self.block_size, j * self.block_size, self.block_size, self.block_size), 1)

            # Show the next block on the next_block_screen-----------------------#
            self.display_next_block()

            # Display the current block and update its position-----------------------#
            self.update_block_position()
            self.display_block()

            # Draw the placed blocks on the board----------------------------#
            self.draw_board()

            # Key binding-----------------------------#
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.run = False

                if event.type == KEYDOWN:
                    if event.key == K_a:
                        if not self.check_side_collision(-1):
                            self.block_pos[0] -= 1
                            self.press_sound.play()
                    if event.key == K_f:
                        if not self.check_side_collision(1):
                            self.block_pos[0] += 1
                            self.press_sound.play()
                    if event.key == K_w or event.key == K_UP:
                        self.rotate_block()
                        self.press_sound.play()

                if event.type == MOUSEBUTTONDOWN:
                    self.rotate_block()
                    self.press_sound.play()

            # Surfaces blit to the main screen-------------------------#
            self.screen.blit(self.game_surface, [self.padding, self.padding])
            self.screen.blit(self.next_surface,
                             [self.game_surface.get_width() + 2 * self.padding, self.padding])
            self.screen.blit(self.score_surface, [self.game_surface.get_width() + 2 * self.padding,
                                                  self.next_surface.get_height() + 2 * self.padding])
            pygame.display.update()
            self.clock.tick(self.fps)

        pygame.quit()


if __name__ == "__main__":
    game = Game()
    game.display_home_screen()
