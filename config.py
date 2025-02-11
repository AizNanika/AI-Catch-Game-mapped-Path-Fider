"""
Zentrale Konfigurationsdatei für das Spiel.
Enthält alle wichtigen Konstanten und Einstellungen.
"""
from collections import namedtuple

# Farbdefinitionen (RGB)
WHITE = (255, 255, 255)
RED = (200, 0, 0)
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
BLACK = (0, 0, 0)
GREY = (100, 100, 100)
LESS_GREEN = (0, 200, 0)  # Helleres Grün für UI-Text

# Spieleinstellungen
SPEED = 60  # Spielgeschwindigkeit in FPS
BLOCK_SIZE = 30  # Größe eines Spielfeldelements in Pixeln
STANDARD_PENALTY = -10  # Standardbestrafung für Kollisionen
STANDARD_REWARD = 10  # Standardbelohnung für Erfolge
FONT_SIZE = 25  # Schriftgröße für UI-Elemente

# Spielfeldgrößen
WIDTH = 900  # Spielfeldbreite in Pixeln
HEIGHT = 900  # Spielfeldhöhe in Pixeln

# Spielmoduseinstellungen
render = True  # Aktiviert/Deaktiviert die grafische Darstellung
use_clock = False  # Aktiviert/Deaktiviert die Geschwindigkeitsbegrenzung
debug_mode = True  # Aktiviert/Deaktiviert Debug-Informationen
use_heat_map = False  # Aktiviert/Deaktiviert die Heatmap-Visualisierung

# Startposition
START_X = 5 * BLOCK_SIZE
START_Y = 5 * BLOCK_SIZE

# Hilfsdatentyp für Koordinaten
Point = namedtuple('Point', 'x, y')


