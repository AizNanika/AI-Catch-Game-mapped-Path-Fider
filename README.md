# AI-Catch-Game-mapped-Path-Finder
A Project where two AI´s are competing with each other. One of them (blue) is the hunter and its goal is to catch the opponent (red). The clue is, that the red square is running away. Both squares learn from each other and develop tactics to either catch faster or run away better! BASED ON SNAKE!

Dokumentation:

Schritt 1 - Grundgerüst: 
  - Mit Pygame Spielfeld erstellt.
    ` BOARD_WIDTH = 1200
      BOARD_HEIGHT = 1200
      BORDER_THICKNESS = 30
      boarder_y_down = BOARD_HEIGHT - 30
      boarder_y_up = 30
      boarder_x_left = BOARD_WIDTH - 30` 
  - Quadrat eingefügt (Blau), Punkt eingefügt (Rot)
    ` width = grid_size
      height = grid_size
      food_size = grid_size`
  - Definiert, dass Blau der Fänger sein soll und Rot das zu errerichende Ziel
  - Blau ist durch Spieler Steuerbar
` press = pygame.key.get_pressed()
    if press[arrow_up]:
        y -= speed
    elif press[arrow_down]:
        y += speed
    elif press[arrow_left]:
        x -= speed
    elif press[arrow_right]:
        x += speed   `
  - Score und Koordinaten werden in Kopf- und Fußzeile angezeigt
    `self.draw_text(f"X: {x}", text_font, green, 2, BOARD_HEIGHT - 20)
     lf.draw_text(f"Y: {y}", text_font, green, 80, BOARD_HEIGHT - 20)
     self.draw_text(f"FPS: {fps}", text_font, green, 160, BOARD_HEIGHT - 20)`
  - Spielfeldränder definiert -> Man kann nicht außerhalb des Spielfeldes gehen
    `grid_size = 30
     grid_width = BOARD_WIDTH // grid_size
     grid_height = BOARD_HEIGHT // grid_size`
  - Ziel definiert: Roter Punkt soll eingesammelt werden - dient um Erfolg zu messen

Schritt 2 - Objekte:
  - Objekte eingefügt
  - Mehrere Versionen der Objekte im Spielfeld entwickelt
  - Objekte für zukünftige Fortschritte angepasst
`   [{obstacles = 
    {"x": 9 * grid_size, "y": 2 * grid_size, "width": grid_size, "height": 15 * grid_size},
    {"x": 19 * grid_size, "y": 2 * grid_size, "width": grid_size, "height": 15 * grid_size},
    {"x": 18 * grid_size, "y": 22 * grid_size, "width": grid_size, "height": 15 * grid_size},
    {"x": 29 * grid_size, "y": 2 * grid_size, "width": grid_size, "height": 9 * grid_size},
    {"x": 29 * grid_size, "y": 15 * grid_size, "width": grid_size, "height": 20 * grid_size},
    {"x": 3 * grid_size, "y": 9 * grid_size, "width": 12 * grid_size, "height": grid_size},
    {"x": 22 * grid_size, "y": 9 * grid_size, "width": 14 * grid_size, "height": grid_size},
    {"x": 0 * grid_size, "y": 19 * grid_size, "width": 16 * grid_size, "height": grid_size},
    {"x": 22 * grid_size, "y": 19 * grid_size, "width": 13 * grid_size, "height": grid_size},
    {"x": 6 * grid_size, "y": 29 * grid_size, "width": 30 * grid_size, "height": grid_size}]`


Schritt 3 - Movement:
  - Blauer Punkt bewegt sich zufällig
`   random_pt = (random.randint(0, boarder_x_left), random.randint(boarder_y_up, boarder_y_down))
    random_pos = (random.randint(0, boarder_x_left), random.randint(boarder_y_up, boarder_y_down))
    food_pos = random_pos`
  - Blauer Punkt bewegt sich auf direktem Weg zu Rotem Punkt. Ignoriert dabei Objekte
  - Roter Punkt weiterhin statisch
      - Blauer Punkt bewegt sich durch Algorithmus zum Roten Punkt hin
        - direkt mit A* gelöst. Somit ist entsprechender Code später zu sehen. Siehe Schritt 4!  
      - geht noch durch Objekte durch
          - Bugs gefixt, Blauer Punkt beachtet Objekte und umgeht diese
          - Roter Punkt kann nicht zufällig in Objekt spawnen (2 Pixel Abstand)

Schritt 4 - A* Blauer Punkt:
  - Blauer Punkt findet Weg mit A*
`def a_star(start, goal, obstacles, grid_size, grid_width, grid_height):
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
    return []`
  - Debug Methode implementiert
`       def debug(self):
        self.draw_text(f"X: {x}", pygame.font.SysFont(None, 30), green, 2, BOARD_HEIGHT - 20)
        self.draw_text(f"Y: {y}", pygame.font.SysFont(None, 30), green, 80, BOARD_HEIGHT - 20)
        self.draw_text(f"FPS: {fps}", pygame.font.SysFont(None, 30), green, 160, BOARD_HEIGHT - 20)
        self.draw_text(f"Score: {score}", pygame.font.SysFont(None, 30), green, 0, 6)`

Schritt 5 - Essen:
  - Essen aktualisiert jede Sekunde die Position
    - sucht sich eine zufällige Position auf Spielfeld
    - Blauer Punkt reagiert in Echtzeit darauf und berechnet den zu laufenden Weg neu
      def generate_food_pos():
`       while True:
        pos = (random.randint(0, boarder_x_left - 30), random.randint(boarder_y_up, boarder_y_down - 30))
        food_rect = pygame.Rect(pos[0], pos[1], 30, 30)
        if not any(food_rect.colliderect(pygame.Rect(obstacle["x"], obstacle["y"], obstacle["width"], obstacle["height"])) for obstacle in obstacles):
            return pos
food_pos = generate_food_pos()`
  - Essen Steuerbar durch Spieler
    - Durch neue Methoden `(food_speed_x, food_speed_y)` und Ereignisbehandlungen `(pygame.KEYDOWN)` die Bewegungen des Essens ermöglicht
    - Funktion `is_collision_with_obstacle` überprüft, ob das Essen bei Bewegung auf ein Hindernis trifft
    - Die Bewegungslogik für Essen berücksichtigt jetzt Schritt-für-Schritt-Kollisionen, um realistische Bewegungen sicherzustellen. Um sicherzustellen, dass das Essen nur an gültigen Positionen innerhalb des Spielfelds bleibt und nicht durch Hindernisse bewegt werden kann
  - Zufällige Bewegnung des Essens
    - Entfernt: `def move_food_with_collision(food_pos, food_speed_x, food_speed_y)`
    - Bewegung mit menschlicher Steuerung: Zeile 228
    - `print(food_pos)` : Zeile 269
    - Hinzugefügt: `def move_food_randomly(food_pos)`
    - Angepasst:  `od_pos = move_food_randomly(food_pos)` Zeile 213

Schritt 6 - Plotting:
  - Diagramm erstellt, welches anzeigt, wie oft Essen in bestimmter Zeit gefangen wurde (Visualisiert) 
`   import matplotlib.pyplot as plt 
    def plot(scores):
    """
    Plottet die Scores und den Durchschnitt über alle Spiele.
    """
    x = list(range(1, len(scores) + 1))  # Spiele
    cumulative_mean = [sum(scores[:i + 1]) / (i + 1) for i in range(len(scores))]  # Durchschnitts-Scores
    plt.clf()
    plt.plot(x, scores, marker="o", label="Scores")
    plt.plot(x, cumulative_mean, linestyle="--", color="orange", label="Durchschnittlicher Score")
    plt.title("Scores und Durchschnittlicher Score über die Spiele")
    plt.xlabel("Spiele")
    plt.ylabel("Scores")
    plt.legend()
    plt.grid(True)
    plt.show(block=False)
    plt.pause(0.1)`

  - Für mehrere Spielversionen angefertigt
      - A*
      - Random Movement
      - Menschliche Stuerung des Essens
  - auf ältere Versionen angewandt um zu vergleichen

Schritt 7: A* Roter Punkt:
  - Essen sucht sich den am weitesten entfernten Punkt vom Fänger und wandert mit A* dorthin
    - prüft in Echtzeit ob Bewegung zulässig ist
      `path = a_star(food_start, furthest_point, obstacles, grid_size, grid_width * grid_size, grid_height * grid_size)`
