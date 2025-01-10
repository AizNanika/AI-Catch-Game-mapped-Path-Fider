"""
Hier werden alle Konstanten oder genutzten Variablen gespeichert.
"""


# RGB Farben
WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0,0,0)
GREEN = (0, 255, 0)
LESS_GREEN = (14, 150, 10)

# Konstanten
SPEED = 60 # Steuert die Clock, die die geschwindigkeit des Spiels manipuliert
BLOCK_SIZE = 30 # Größe der Grid
STANDARD_PENALTY = -10 # Standard Bestrafungswert
STANDARD_REWARD = 10 # Standard Belohnungswert
FONT_SIZE = 25


# WIDTH und HEIGHT muss ein Vielfaches von BLOCK_SIZE sein, sonst funktioniert das game nicht
WIDTH = 1200
HEIGHT = 1200
boarder_y_down = HEIGHT - BLOCK_SIZE
boarder_y_up = BLOCK_SIZE
boarder_x_left = WIDTH - BLOCK_SIZE

