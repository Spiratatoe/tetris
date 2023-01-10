"""
Jack Spiratos, 1930720
Robert Vincent
Programming Techniques and Paradigms, 420-LCW-MS section 1
May 7, 2021
Final Project
"""

import pygame
from pygame import mixer

from colours import Colours, shape_colours
from pieces import get_shape


# Variables
s_width = 1200
s_height = 650
play_width = 300
play_height = 600
block_size = 30  # 300//10

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

# Functions for menu decorations --------------------------------------


def draw_text_middle(text, size, colour, surface):
    font = pygame.font.SysFont("freesansbold.ttf", size, bold=True)
    label = font.render(text, 1, colour)

    surface.blit(
        label,
        (
            top_left_x + play_width // 2 - label.get_width() // 2,
            top_left_y + play_height // 2 - label.get_height() // 2,
        ),
    )


def draw_tetris_logo(surface):
    logo = pygame.image.load("The_Tetris_Company_logo.png")
    sx = top_left_x - 35
    sy = top_left_y + 25

    surface.blit(logo, (sx, sy))


# -----------------------------------------------------------------------


def draw_grid(surface, grid):
    sx = top_left_x
    sy = top_left_y

    for i in range(len(grid)):
        pygame.draw.line(
            surface,
            Colours.GRAY,
            (sx, sy + i * block_size),
            (sx + play_width, sy + i * block_size),
        )
        for j in range(len(grid[i])):
            pygame.draw.line(
                surface,
                Colours.GRAY,
                (sx + j * block_size, sy),
                (sx + j * block_size, sy + play_height),
            )


class DrawClass:
    def __init__(self, surface):
        self.surface = surface
        self.logo = pygame.image.load("Optimized-Tetris_logo.png")

        self.font_100 = pygame.font.SysFont("freesansbold.ttf", 100)
        self.font_60 = pygame.font.SysFont("freesansbold.ttf", 60)
        self.font_50 = pygame.font.SysFont("freesansbold.ttf", 50)
        self.font_40 = pygame.font.SysFont("freesansbold.ttf", 40)
        self.font_30 = pygame.font.SysFont("freesansbold.ttf", 30)

        self.blocks = []
        colours = ["green", "red", "cyan", "yellow", "orange", "blue", "purple"]
        for colour in colours:
            img = pygame.image.load(f"blocks/clean_{colour}.png")
            self.blocks.append(img)

    def draw_window(self, grid, score, high_score, lines):
        surface = self.surface

        surface.fill(Colours.BLACK)

        sx = top_left_x - 340
        sy = top_left_y + 25
        surface.blit(self.logo, (sx, sy))

        # current score
        current_score = self.font_60.render("Score:" + str(score), 1, Colours.PINK)

        sx = top_left_x + play_width + 50
        sy = top_left_y + play_height // 2 - 100
        surface.blit(current_score, (sx + 60, sy + 60))

        # High Score
        high_score = self.font_60.render("High Score:" + high_score, 1, Colours.RED)

        sx = top_left_x - 400
        sy = top_left_y + 175
        surface.blit(high_score, (sx, sy))

        # HELP
        label = self.font_100.render("H E L P", 1, Colours.ORANGE)

        sx = top_left_x - 380
        sy = top_left_y + 225
        surface.blit(label, (sx, sy))

        #pause 
        label = self.font_30.render("                  p         : Pause ", 1, Colours.WHITE)

        sx = top_left_x - 390
        sy = top_left_y + 380
        surface.blit(label, (sx, sy))
        # controls
        label = self.font_30.render("Upwards Arrow     : ROTATE ", 1, Colours.YELLOW)

        sx = top_left_x - 390
        sy = top_left_y + 300
        surface.blit(label, (sx, sy))
        # -----------------------------------------------
        label = self.font_30.render("Downwards Arrow: SPEED UP", 1, Colours.GREEN)

        sx = top_left_x - 390
        sy = top_left_y + 320
        surface.blit(label, (sx, sy))
        # -------------------------------------------------
        label = self.font_30.render("Rightwards Arrow : RIGHT", 1, Colours.CYAN)

        sx = top_left_x - 390
        sy = top_left_y + 340
        surface.blit(label, (sx, sy))
        # -------------------------------------------------
        label = self.font_30.render("Leftwards Arrow   : LEFT", 1, Colours.PURPLE)

        sx = top_left_x - 390
        sy = top_left_y + 360
        surface.blit(label, (sx, sy))
        # -------------------------------------------------

        # Lines Destroyed
        label = self.font_40.render("Lines Destroyed:" + str(lines), 1, Colours.YELLOW)

        sx = top_left_x + play_width + 50
        sy = top_left_y + play_height // 2
        surface.blit(label, (sx + 60, sy + 60))

        # ----------------------------------------------------------

        # Drawing the blocks
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j] != Colours.BLACK:
                    self.draw_block(grid[i][j], j, i)

        # Border of the grid
        pygame.draw.rect(
            surface, Colours.RED, (top_left_x, top_left_y, play_width, play_height), 4
        )

        draw_grid(surface, grid)

        # Draw the next piece text
        label = self.font_50.render("Next Shape:", 1, Colours.PALEGREEN)
        sx = top_left_x + play_width + 90
        sy = top_left_y + play_height // 2 - 250
        surface.blit(label, (sx + 10, sy - 30))


    def draw_block(self, colour, x, y):
        x = top_left_x + x * block_size
        y = top_left_y + y * block_size
        # pygame.draw.rect(self.surface, colour, (x, y, block_size, block_size), 0)

        index = shape_colours.index(colour)
        self.surface.blit(self.blocks[index], (x, y))


def convert_shape_format(piece):
    """
    makes shapes readable for the computer
    returns a list of coordinates as tuples
    """
    positions = []
    # Get the list of str representing the current rotated shape
    fmt = piece.shape[piece.rotation % len(piece.shape)]

    for i, line in enumerate(fmt):
        for j, column in enumerate(line):
            if column == "0":
                positions.append((piece.x + j - 2, piece.y + i - 4))

    return positions


def update_score(nscore):
    score = max_score()

    with open("scores.txt", "r") as f:
        lines = f.readlines()
        score = lines[0].strip()

    with open("scores.txt", "w") as f:
        if int(score) > nscore:
            f.write(str(score))
        else:
            f.write(str(nscore))


def max_score():
    with open("scores.txt", "r") as f:
        lines = f.readlines()
        score = lines[0].strip()

    return score


"""
////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
"""


class GameClass:
    def __init__(self):
        self.grid = self.create_grid()
        self.last_score = max_score()
        self.paused = False
        self.score = 0
        self.lines_deleted = 0
        self.game_over = False

        self.current_piece = get_shape()
        self.next_piece = get_shape()
        self.clock = pygame.time.Clock()
        self.fall_time = 0
        self.fall_speed = 0.25
        self.level_time = 0

        self.draw_class = DrawClass(win)

        self.keys_cooldown = {}

        mixer.music.load("Sound.ogg")
        mixer.music.play(-1)

    def create_grid(self):
        """create a 10 blocks for every row (20 in total)"""
        grid = [[Colours.BLACK for x in range(10)] for x in range(20)]
        return grid

    def valid_space(self, shape):
        """tells you if you can move here or not"""
        formatted = convert_shape_format(shape)

        for (x, y) in formatted:
            if y >= 20 or x < 0 or x >= 10:
                return False
            if x >= 0 and y >= 0 and self.grid[y][x] != Colours.BLACK:
                return False
        return True

    def clear_rows(self):
        rows_to_delete = [
            i for i, row in enumerate(self.grid) if row.count(Colours.BLACK) == 0
        ]

        for row in rows_to_delete[::-1]:
            self.grid.pop(row)

        new_lines = [[Colours.BLACK] * 10 for _ in range(len(rows_to_delete))]
        self.grid = new_lines + self.grid

        # Update the score and the number of lines deleted
        self.score += (len(rows_to_delete) ** 2) * 240
        self.lines_deleted += len(rows_to_delete)

    def user_input(self, current_piece):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True

            if event.type != pygame.KEYDOWN:
                continue

            if event.key == pygame.K_p:
                self.paused = not self.paused

        if self.paused:
            return

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.on_cooldown(pygame.K_LEFT):
            current_piece.x -= 1
            if not (self.valid_space(current_piece)):
                current_piece.x += 1
        if keys[pygame.K_RIGHT] and self.on_cooldown(pygame.K_RIGHT):
            current_piece.x += 1
            if not (self.valid_space(current_piece)):
                current_piece.x -= 1
        if keys[pygame.K_DOWN] and self.on_cooldown(pygame.K_DOWN):
            current_piece.y += 1
            if not (self.valid_space(current_piece)):
                current_piece.y -= 1
        if keys[pygame.K_UP] and self.on_cooldown(pygame.K_UP):
            current_piece.rotation += 1
            if not (self.valid_space(current_piece)):
                current_piece.rotation -= 1

    def on_cooldown(self, key):
        now = pygame.time.get_ticks()
        cooldown = self.keys_cooldown.get(key, 0)
        cooldown_amount = 150

        if now > cooldown + cooldown_amount:
            self.keys_cooldown[key] = now
            return True

        return False

    def update_ticks(self):
        # better than the FPS method in the source code
        self.fall_time += self.clock.get_rawtime()
        self.level_time += self.clock.get_rawtime()
        self.clock.tick()

    def update(self):
        if self.fall_time / 1000 > self.fall_speed:
            self.fall_time = 0
            self.current_piece.y += 1
            if not self.valid_space(self.current_piece) and self.current_piece.y > 0:
                self.current_piece.y -= 1
                self.change_piece()
                return

        self.shape_pos = convert_shape_format(self.current_piece)

    def change_piece(self):
        self.shape_pos = convert_shape_format(self.current_piece)

        for pos in self.shape_pos:
            x, y = pos[0], pos[1]
            if y < 0:
                self.lose()
                return

            self.grid[y][x] = self.current_piece.colour

        self.current_piece = self.next_piece
        self.next_piece = get_shape()

        self.clear_rows()

        # if the new piece is not in a valid space, the player lose
        if not self.valid_space(self.current_piece):
            self.lose()

    def lose(self):
        draw_text_middle("YOU LOST", 100, Colours.WHITE, win)
        pygame.display.update()
        mixer.music.stop()
        pygame.time.delay(2000)
        self.game_over = True
        update_score(self.score)

    def run(self):
        while not self.game_over:
            self.update_ticks()

            self.user_input(self.current_piece)
            if not self.paused:
                self.update()

            self.draw()

    def draw(self):
        self.draw_class.draw_window(
            self.grid,
            self.score,
            self.last_score,
            self.lines_deleted,
        )

        # Drawing the current piece into the grid
        for (x, y) in self.shape_pos:
            self.draw_class.draw_block(self.current_piece.colour, x, y)

        next_shape_pos = convert_shape_format(self.next_piece)
        for (x, y) in next_shape_pos:
            self.draw_class.draw_block(self.next_piece.colour, x + 10, y + 8)

        if self.paused:
            draw_text_middle("PAUSED", 100, Colours.WHITE, win)

        pygame.display.update()


def main_menu():
    # ! main menu has unlimited fps
    while True:
        # User input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                game = GameClass()
                game.run()

        # Draw
        win.fill(Colours.BLACK)
        draw_text_middle("Press any key to begin.", 60, Colours.WHITE, win)
        draw_tetris_logo(win)
        pygame.display.update()


pygame.font.init()  # initializes the font module, so it works later on
mixer.init()
pygame.init()

win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption("Tetris")
main_menu()  # start game
