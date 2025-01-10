import pygame
import random
import numpy as np

from config import *
from obstacles import obstacles
from directions import Direction
from collections import namedtuple

pygame.init()
#font = pygame.font.Font('arial.ttf', FONT_SIZE)
font = pygame.font.SysFont('arial', FONT_SIZE)

Point = namedtuple('Point', 'x, y')

class CatchGameEnv:

    def __init__(self):
        self.w = WIDTH
        self.h = HEIGHT
        # init display
        self.display = pygame.display.set_mode((self.w, self.h))
        pygame.display.set_caption('Catch the Food - AI-Agent version')
        self.clock = pygame.time.Clock()
        self.reset()

    def get_block_size(self):
        return BLOCK_SIZE

    def reset(self):
        self.direction = Direction.RIGHT
        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0
        self.head = Point(self.w // 2, self.h // 2)  # Nur der Kopf

    def _place_food(self):
        x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        self.food = Point(x, y)

    def play_step(self, action):
        self.frame_iteration += 1
        # 1. collect user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        # 2. move
        self._move(action)
        
        # 3. check if game over
        reward = 0
        game_over = False
        if self.is_collision() or self.frame_iteration > 200:
            game_over = True
            reward = STANDARD_PENALTY
            return reward, game_over, self.score

        # 4. place new food or just move
        if self.head == self.food:
            self.score += 1
            reward = STANDARD_REWARD
            self.frame_iteration = 0
            self._place_food()
        
        # 5. update ui and clock
        self._update_ui()
        self.clock.tick(SPEED)
        # 6. return game over and score
        return reward, game_over, self.score

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        # Prüfe nur, ob der Kopf die Grenzen trifft
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        return False

    def _update_ui(self):
        self.display.fill(BLACK)

        # Zeichne den Kopf
        pygame.draw.rect(self.display, BLUE1, pygame.Rect(self.head.x, self.head.y, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(self.display, BLUE2, pygame.Rect(self.head.x + 4, self.head.y + 4, 12, 12))

        # Zeichne das Essen
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def _move(self, action):
        # action ist eine Liste: [Links, Rechts, Oben, Unten]
        directions = {
            0: Direction.LEFT,
            1: Direction.RIGHT,
            2: Direction.UP,
            3: Direction.DOWN
        }

        # Setze die Richtung basierend auf der Aktion
        self.direction = directions[np.argmax(action)]

        # Aktuelle Kopfposition
        x, y = self.head.x, self.head.y

        # Bewegung basierend auf Richtung
        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)

