import heapq

import pygame
import random
import numpy as np
from config import *
from obstacles__ import obstacles
from directions import Direction

pygame.init()
#font = pygame.font.Font('arial.ttf', FONT_SIZE)
font = pygame.font.SysFont('arial', FONT_SIZE)

class CatchGameEnv:

    def __init__(self):
        self.w = WIDTH
        self.h = HEIGHT
        self.steps = 0
        # init display
        self.display = pygame.display.set_mode((self.w, self.h),pygame.RESIZABLE)
        pygame.display.set_caption('Catch the Food - AI-Agent version')
        self.clock = pygame.time.Clock()
        self.debug = debug_mode
        # Heatmap: 2D-Array mit Nullen (Anzahl Besuche pro Feld)
        self.heatmap = np.zeros((self.w // BLOCK_SIZE, self.h // BLOCK_SIZE))
        self.heatmap_enabled = use_heat_map  # Heatmap an/aus-Schalter
        self.reset()

    def toggle_heatmap(self):
        """Schaltet die Heatmap an oder aus."""
        self.heatmap_enabled = not self.heatmap_enabled

    def toggle_debug_mode(self):
        self.debug = not self.debug

    def get_block_size(self):
        return BLOCK_SIZE

    def reset(self):
        self.heatmap.fill(0)  # Heatmap bei Spielneustart leeren
        self.direction = Direction.RIGHT
        self.score = 0
        self.food = None
        self._place_food()
        self.frame_iteration = 0
        self.steps = 0
        self.head = Point(self.w // 2, self.h // 2)  # Nur der Kopf
        self.heatmap[self.head.x // BLOCK_SIZE, self.head.y // BLOCK_SIZE] += 1

    def _place_food(self):
        while True:
            x = random.randint(0, (self.w - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            y = random.randint(0, (self.h - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            new_food = Point(x, y)

            # Prüfen, ob das Essen auf einem Hindernis liegt
            collision = False
            for obstacle in obstacles:
                if obstacle["x"] <= new_food.x < obstacle["x"] + obstacle["width"] and \
                        obstacle["y"] <= new_food.y < obstacle["y"] + obstacle["height"]:
                    collision = True
                    break

            # Falls keine Kollision mit einem Hindernis, das Essen platzieren
            if not collision:
                self.food = new_food
                break

    def play_step(self, action):
        self.frame_iteration += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_h:
                    self.heatmap_enabled = not self.heatmap_enabled  # Heatmap umschalten

        prev_distance = abs(self.head.x - self.food.x) + abs(self.head.y - self.food.y)
        self._move(action)
        new_distance = abs(self.head.x - self.food.x) + abs(self.head.y - self.food.y)

        reward = -0.005  # Kleinere Strafe für jeden Schritt
        game_over = False

        if self.is_collision() or self.frame_iteration > 200:
            reward = -1  # Hohe Strafe für Kollisionen mit Hindernissen oder Wänden
            game_over = True
            return reward, game_over, self.score, self.steps

        if new_distance < prev_distance:
            reward += 0.1  # Belohnung für Annäherung an das Essen

        if self.heatmap[self.head.x // BLOCK_SIZE, self.head.y // BLOCK_SIZE] > 1:
            reward -= 0.05  # Strafe für wiederholtes Betreten des gleichen Bereichs

        if self.head == self.food:
            self.steps += self.frame_iteration
            self.score += 1
            reward = 1  # Belohnung für das Erreichen des Essens
            self.frame_iteration = 0
            self._place_food()
            self.heatmap.fill(0)

        if render:
            self._update_ui()

        if use_clock:
            self.clock.tick(SPEED)

        return reward, game_over, self.score, self.steps

    def is_collision(self, pt=None):
        if pt is None:
            pt = self.head
        # Prüfe auf Kollision mit Spielfeldgrenzen
        if pt.x > self.w - BLOCK_SIZE or pt.x < 0 or pt.y > self.h - BLOCK_SIZE or pt.y < 0:
            return True
        # Prüfe auf Kollision mit Hindernissen
        for obstacle in obstacles:
            if obstacle["x"] <= pt.x < obstacle["x"] + obstacle["width"] and \
                    obstacle["y"] <= pt.y < obstacle["y"] + obstacle["height"]:
                return True
        return False

    def _update_ui(self):
        self.display.fill(BLACK)

        # Zeichne Hindernisse
        for obstacle in obstacles:
            pygame.draw.rect(self.display, GREY,
                             pygame.Rect(obstacle["x"], obstacle["y"], obstacle["width"], obstacle["height"]))
        # Zeichne den Fänger
        pygame.draw.rect(self.display, BLUE1, pygame.Rect(self.head.x, self.head.y, BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(self.display, BLUE2, pygame.Rect(self.head.x + 4, self.head.y + 4, 12, 12))

        # Zeichne das Essen
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))

        if self.debug:
            self._draw_text(f"X: {self.head.x}", (10, 50), color=LESS_GREEN, font_size=FONT_SIZE)
            self._draw_text(f"Y: {self.head.y}", (10, 80), color=LESS_GREEN, font_size=FONT_SIZE)
            self._draw_text(f"Food X: {self.food.x}", (10, 110), color=LESS_GREEN, font_size=FONT_SIZE)
            self._draw_text(f"Food Y: {self.food.y}", (10, 140), color=LESS_GREEN, font_size=FONT_SIZE)

            if self.heatmap_enabled:
                max_visits = np.max(self.heatmap) if np.max(self.heatmap) > 0 else 1
                for x in range(self.heatmap.shape[0]):
                    for y in range(self.heatmap.shape[1]):
                        intensity = int((self.heatmap[x, y] / max_visits) * 255)  # Normierung auf 0-255
                        if intensity > 0:
                            pygame.draw.rect(self.display, (0, 0, intensity, 100),  # Rote Farbskala
                                             pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

        self._draw_text("Score: " + str(self.score), (0, 0), color=WHITE, font_size=FONT_SIZE)

        optimal_steps = self.get_optimal_steps()
        self.optimal_steps = optimal_steps  # Speichern für spätere Analyse

        pygame.display.flip()

    def get_optimal_steps(self):
        """ Berechnet die optimale Anzahl an Schritten mit A* """
        path = a_star(self.head, self.food, obstacles, self.w, self.h, self.get_block_size())
        if path:
            return len(path) - 1  # Pfadlänge in Schritte umrechnen
        else:
            return 0  # Falls kein Pfad gefunden wurde

    def _draw_text(self, text, position, color=(255, 255, 255), font_size=FONT_SIZE):
        # Zeichnet Text auf dem Bildschirm
        img = font.render(text, True, color)  # Gibt ein gerendertes Bild des Textes zurück
        self.display.blit(img, position)  # Zeichnet den Text auf den Bildschirm

    def _move(self, action):
        directions = {
            0: Direction.LEFT,
            1: Direction.RIGHT,
            2: Direction.UP,
            3: Direction.DOWN
        }

        self.direction = directions[np.argmax(action)]
        x, y = self.head.x, self.head.y

        if self.direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif self.direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif self.direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif self.direction == Direction.UP:
            y -= BLOCK_SIZE

        self.head = Point(x, y)

        # Heatmap aktualisieren
        heat_x = x // BLOCK_SIZE
        heat_y = y // BLOCK_SIZE

        if 0 <= heat_x < self.heatmap.shape[0] and 0 <= heat_y < self.heatmap.shape[1]:
            self.heatmap[heat_x, heat_y] += 1


def heuristic(a, b):
    """Berechnet die Manhattan-Distanz als Heuristik."""
    return abs(a.x - b.x) + abs(a.y - b.y)


def a_star(start, goal, obstacles, width, height, block_size):
    """
    Implementiert den A*-Algorithmus zur Berechnung des optimalen Pfads.

    :param start: Startposition (Point)
    :param goal: Zielposition (Point)
    :param obstacles: Liste von Hindernissen
    :param width: Spielfeldbreite
    :param height: Spielfeldhöhe
    :param block_size: Größe eines Blocks
    :return: Liste von Punkten, die den optimalen Pfad repräsentieren
    """
    open_list = []  # Prioritätswarteschlange
    heapq.heappush(open_list, (0, start))
    came_from = {start: None}  # Rückverfolgung des Pfads
    g_score = {start: 0}  # Kosten vom Startpunkt
    f_score = {start: heuristic(start, goal)}  # Geschätzte Gesamtkosten

    directions = [
        Point(0, -block_size),  # Oben
        Point(0, block_size),  # Unten
        Point(-block_size, 0),  # Links
        Point(block_size, 0)  # Rechts
    ]

    def is_valid(point):
        """Prüft, ob der Punkt im gültigen Bereich und nicht in einem Hindernis liegt."""
        if point.x < 0 or point.y < 0 or point.x >= width or point.y >= height:
            return False
        for obs in obstacles:
            if obs["x"] <= point.x < obs["x"] + obs["width"] and \
                    obs["y"] <= point.y < obs["y"] + obs["height"]:
                return False
        return True

    while open_list:
        _, current = heapq.heappop(open_list)

        if current == goal:
            path = []
            while current is not None:
                path.append(current)
                current = came_from[current]
            return path[::-1]  # Pfad umkehren

        for direction in directions:
            neighbor = Point(current.x + direction.x, current.y + direction.y)
            if not is_valid(neighbor):
                continue

            tentative_g_score = g_score[current] + 1
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(open_list, (f_score[neighbor], neighbor))

    return []  # Kein Pfad gefunden
