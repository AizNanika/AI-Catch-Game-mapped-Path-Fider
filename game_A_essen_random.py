import pygame
import sys
import random
import math
from plot_helper import plot  # Importiere die ausgelagerte Plot-Funktion

# pygame initialisieren
pygame.init()

# field size
BOARD_WIDTH = 1200
BOARD_HEIGHT = 1200
BORDER_THICKNESS = 30
boarder_y_down = BOARD_HEIGHT - 30
boarder_y_up = 30
boarder_x_left = BOARD_WIDTH - 30

# Grid-Größe definieren
grid_size = 30
grid_width = BOARD_WIDTH // grid_size
grid_height = BOARD_HEIGHT // grid_size

# Hindernisse auf ein Grid-System setzen
obstacles = [
    {"x": 9 * grid_size, "y": 2 * grid_size, "width": grid_size, "height": 15 * grid_size},
    {"x": 19 * grid_size, "y": 2 * grid_size, "width": grid_size, "height": 15 * grid_size},
    {"x": 18 * grid_size, "y": 22 * grid_size, "width": grid_size, "height": 15 * grid_size},
    {"x": 29 * grid_size, "y": 2 * grid_size, "width": grid_size, "height": 9 * grid_size},
    {"x": 29 * grid_size, "y": 15 * grid_size, "width": grid_size, "height": 20 * grid_size},
    {"x": 3 * grid_size, "y": 9 * grid_size, "width": 12 * grid_size, "height": grid_size},
    {"x": 22 * grid_size, "y": 9 * grid_size, "width": 14 * grid_size, "height": grid_size},
    {"x": 0 * grid_size, "y": 19 * grid_size, "width": 16 * grid_size, "height": grid_size},
    {"x": 22 * grid_size, "y": 19 * grid_size, "width": 13 * grid_size, "height": grid_size},
    {"x": 6 * grid_size, "y": 29 * grid_size, "width": 30 * grid_size, "height": grid_size}
]


# zufällige Punkte für Essen (nur an gültigen Positionen)
def generate_food_pos():
    while True:
        pos = (random.randint(0, boarder_x_left - 30), random.randint(boarder_y_up, boarder_y_down - 30))
        food_rect = pygame.Rect(pos[0], pos[1], 30, 30)
        if not any(
                food_rect.colliderect(pygame.Rect(obstacle["x"], obstacle["y"], obstacle["width"], obstacle["height"]))
                for obstacle in obstacles):
            return pos


food_pos = generate_food_pos()

# Farben definieren
screen = pygame.display.set_mode([BOARD_WIDTH, BOARD_HEIGHT])
pygame.display.set_caption("Catch Game with A* Algorithm")
boarder_color = (227, 0, 255)
player_color = (99, 118, 245)
food_color = (255, 0, 0)
green = (28, 255, 0)

# clock
clock = pygame.time.Clock()

# start-position of catcher
x = 300
y = 300

# score
score = 0

# character size
width = grid_size
height = grid_size
food_size = grid_size

# framerate
fps = 60


# Funktion zur Überprüfung, ob der Punkt kollidiert
def check_collision(x, y):
    player_rect = pygame.Rect(x, y, width, height)
    for obstacle in obstacles:
        obstacle_rect = pygame.Rect(obstacle["x"], obstacle["y"], obstacle["width"], obstacle["height"])
        if player_rect.colliderect(obstacle_rect):
            return True
    return False


# A* Algorithmus Implementierung
def a_star(start, goal, obstacles, grid_size, grid_width, grid_height):
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def get_neighbors(node):
        neighbors = [
            (node[0] + grid_size, node[1]),
            (node[0] - grid_size, node[1]),
            (node[0], node[1] + grid_size),
            (node[0], node[1] - grid_size)
        ]
        valid_neighbors = [
            n for n in neighbors
            if 0 <= n[0] < grid_width and 0 <= n[1] < grid_height and not check_collision(*n)
        ]
        return valid_neighbors

    open_set = set([start])
    came_from = {}
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}

    while open_set:
        current = min(open_set, key=lambda x: f_score.get(x, float('inf')))

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path

        open_set.remove(current)

        for neighbor in get_neighbors(current):
            tentative_g_score = g_score[current] + 1
            if tentative_g_score < g_score.get(neighbor, float('inf')):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                open_set.add(neighbor)

    return []


# Spielfeld-Grid definieren
grid_size = 30
grid_width = BOARD_WIDTH // grid_size
grid_height = BOARD_HEIGHT // grid_size


# Ob man beim Steuern vom Essen gegen eine Kollision stoßt NEU
def is_collision_with_obstacle(x, y):
    food_rect = pygame.Rect(x, y, food_size, food_size)
    for obstacle in obstacles:
        obstacle_rect = pygame.Rect(obstacle["x"], obstacle["y"], obstacle["width"], obstacle["height"])
        if food_rect.colliderect(obstacle_rect):
            return True
    return False


def move_food_randomly(food_pos):
    new_x, new_y = food_pos
    directions = [(0, -grid_size), (0, grid_size), (-grid_size, 0), (grid_size, 0)]  # Oben, unten, links, rechts
    valid_move = False
    while not valid_move:
        dx, dy = random.choice(directions)
        new_x, new_y = food_pos[0] + dx, food_pos[1] + dy
        # Überprüfe, ob die neue Position innerhalb des Spielfelds und nicht in einem Hindernis liegt
        if 0 <= new_x < boarder_x_left and boarder_y_up <= new_y < boarder_y_down - food_size and not is_collision_with_obstacle(
                new_x, new_y):
            valid_move = True
    return new_x, new_y


# Bewegungslogik mit A* Pathfinding
def move_with_a_star(x, y, food_pos):
    start = (x // grid_size * grid_size, y // grid_size * grid_size)
    goal = (food_pos[0] // grid_size * grid_size, food_pos[1] // grid_size * grid_size)

    path = a_star(start, goal, obstacles, grid_size, grid_width * grid_size, grid_height * grid_size)

    if path:
        next_pos = path[0]
        x, y = next_pos
    else:
        print("Pfad nicht gefunden. Zufällige Bewegung ausführen.")
        x, y = x + random.choice([-grid_size, grid_size]), y + random.choice([-grid_size, grid_size])
        while check_collision(x, y):
            x, y = x + random.choice([-grid_size, grid_size]), y + random.choice([-grid_size, grid_size])

    # Blauer Punkt bleibt im Spielfeld
    x = max(0, min(x, BOARD_WIDTH - width))
    y = max(BORDER_THICKNESS, min(y, BOARD_HEIGHT - height - BORDER_THICKNESS))
    return x, y

# Funktion zur Berechnung der Distanz
def distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)

# Funktion zur Auswahl des Punktes mit größtem Abstand zum Fänger
def find_furthest_legal_point(food_pos, catcher_pos):
    directions = [(0, -grid_size), (0, grid_size), (-grid_size, 0), (grid_size, 0)]  # Oben, unten, links, rechts
    max_distance = -1
    best_point = food_pos

    for dx, dy in directions:
        new_x, new_y = food_pos[0] + dx, food_pos[1] + dy
        if 0 <= new_x < boarder_x_left and boarder_y_up <= new_y < boarder_y_down - food_size:
            if not is_collision_with_obstacle(new_x, new_y):
                dist = distance((new_x, new_y), catcher_pos)
                if dist > max_distance:
                    max_distance = dist
                    best_point = (new_x, new_y)

    return best_point

# Bewegungslogik des Essens mit A*
def move_food_with_a_star(food_pos, catcher_pos):
    food_start = (food_pos[0] // grid_size * grid_size, food_pos[1] // grid_size * grid_size)
    catcher_grid_pos = (catcher_pos[0] // grid_size * grid_size, catcher_pos[1] // grid_size * grid_size)

    # Wähle den Punkt mit größter Distanz
    furthest_point = find_furthest_legal_point(food_start, catcher_grid_pos)

    # Berechne den A*-Pfad zum Punkt mit größter Distanz
    path = a_star(food_start, furthest_point, obstacles, grid_size, grid_width * grid_size, grid_height * grid_size)

    if path:
        return path[0]  # Bewege das Essen zum nächsten Punkt im Pfad
    return food_pos  # Falls kein Pfad gefunden wird, bleibt das Essen stehen



# Klasse für das Spiel
class catchGame:
    def draw_text(self, text, font, text_color, x, y):
        img = font.render(text, True, text_color)
        screen.blit(img, (x, y))

    def draw(self):
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, player_color, (x, y, width, height))
        pygame.draw.rect(screen, food_color, (food_pos[0], food_pos[1], food_size, food_size))
        pygame.draw.rect(screen, boarder_color, (0, 0, BOARD_WIDTH, BORDER_THICKNESS))
        pygame.draw.rect(screen, boarder_color, (0, BOARD_HEIGHT - BORDER_THICKNESS, BOARD_WIDTH, BORDER_THICKNESS))
        for obstacle in obstacles:
            pygame.draw.rect(screen, (100, 100, 100),
                             (obstacle["x"], obstacle["y"], obstacle["width"], obstacle["height"]))

    def debug(self):
        self.draw_text(f"X: {x}", pygame.font.SysFont(None, 30), green, 2, BOARD_HEIGHT - 20)
        self.draw_text(f"Y: {y}", pygame.font.SysFont(None, 30), green, 80, BOARD_HEIGHT - 20)
        self.draw_text(f"FPS: {fps}", pygame.font.SysFont(None, 30), green, 160, BOARD_HEIGHT - 20)
        self.draw_text(f"Score: {score}", pygame.font.SysFont(None, 30), green, 0, 6)

def reset():
    global x, y, food_pos, score, moves, games, game_scores
    # Speichere den aktuellen Score
    game_scores.append(score)
    print(f"Game {games + 1}: Reset triggered. Score = {score}")
    
    # Erhöhe die Anzahl der Spiele
    games += 1
    
    # Setze die Position des Fängers zurück
    x, y = 300, 300  # Startposition des Fängers
    
    # Generiere eine neue Position für das Essen
    food_pos = generate_food_pos()
    
    # Zurücksetzen der Punktzahl und Züge
    score = 0
    moves = 0

    # Aktualisiere das Plot
    plot(game_scores)


# Initialisiere zusätzliche Variablen
games = 0
game_scores = []
moves = 0
game_duration = 100  # Timer für jedes Spiel (in Spielzügen)

# Geschwindigkeit für das (steuerbare) weglaufende Essen NEU
speed = grid_size

# Hauptspiel-Schleife
game = catchGame()
run = True

food_move_interval = 2  # Essen bewegt sich nur alle "food_move_interval" Frames

while run:
    # Bewege das Essen nur, wenn der Zähler das Intervall erreicht
    if moves % food_move_interval == 0:
        food_pos = move_food_with_a_star(food_pos, (x, y))
    
    # Bewege den Fänger mit A*
    x, y = move_with_a_star(x, y, food_pos)

    # Kollisionsüberprüfung zwischen Fänger und Essen
    player_rect = pygame.Rect(x, y, width, height)
    food_rect = pygame.Rect(food_pos[0], food_pos[1], food_size, food_size)

    if player_rect.colliderect(food_rect):
        score += 1
        print(f"Score: {score}")
        food_pos = generate_food_pos()
        moves = 0

    moves += 1
    if moves >= game_duration:
        reset()
    
    # Zeichne das Spiel
    game.draw()
    game.debug()
    pygame.display.flip()
    clock.tick(fps)



