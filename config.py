"""
Hier werden alle Konstanten oder global genutzten Variablen des Spiels definiert.
Diese Konfigurationsdatei sorgt dafür, dass wichtige Parameter des Spiels an einem Ort zentralisiert sind.
Dadurch ist es einfacher, Werte zu ändern oder das Verhalten des Spiels anzupassen.
"""
from collections import namedtuple

# --- Farben (als RGB-Tupel definiert) ---
# Weiß: Wird z. B. für den Text (Score-Anzeige) verwendet
WHITE = (255, 255, 255)
# Rot: Z. B. für das Essen im Spiel
RED = (200, 0, 0)
# Blau1 und Blau2: Unterschiedliche Blautöne, z. B. für das Zeichnen des Spielers
BLUE1 = (0, 0, 255)
BLUE2 = (0, 100, 255)
# Schwarz: Hintergrundfarbe des Spiels
BLACK = (0, 0, 0)
# Grün und LESS_GREEN: Kann für visuelle Elemente, wie Hindernisse, verwendet werden
GREEN = (0, 255, 0)
LESS_GREEN = (14, 150, 10)
GREY = (100, 100, 100)


LILA = (230,230,250)
# --- Spielgrundeinstellungen ---
# die Geschwindigkeit des Spiels in Frames pro Sekunde (FPS). Wird von der Clock verwendet, um die Spielframes zu regulieren.
SPEED = 60


# Die Größe eines Blocks (Rasterelement) in Pixel. Die Spielfläche ist in Blöcke aufgeteilt. D.h das die Maßen durch 30 Teilbar sein müssen
BLOCK_SIZE = 30

# Standardbestrafung, die z. B. bei Kollision mit der Wand oder nach Zeitablauf
STANDARD_PENALTY = -10

# Standardbelohnung, die z. B. vergeben wird, wenn der Spieler das Essen erreicht
STANDARD_REWARD = 10

# Die Schriftgröße der Texte, wie z. B. der Score-Anzeige
FONT_SIZE = 25

# --- Spielfeldgrößen ---
# die Breite des Spielfensters in Pixel
WIDTH = 900
# Die Höhe des Spielfensters in Pixel
HEIGHT = 900
# (muss durch block_size teilbar sein → momentan 30)

# Zusätzliche Randbereiche (z. B. für mögliche Kollisionserkennung), basierend auf der Spielfeldgröße
# unterer Spielbereich
boarder_y_down = HEIGHT - BLOCK_SIZE
# Oberer Spielbereich
boarder_y_up = BLOCK_SIZE
# Linker Spielbereich
boarder_x_left = WIDTH - BLOCK_SIZE

# Hinweis: WIDTH und HEIGHT müssen Vielfache von BLOCK_SIZE sein. Da das Spielfeld blockweise aufgebaut ist,
# würde das Spiel sonst nicht korrekt laufen (z. B. könnten die Figur oder das Essen außerhalb des Bereichs platziert werden).

"""
Rendering und Taktsteuerung:
Diese Variablen beeinflussen, ob das Spiel grafisch dargestellt wird und ob die Clock genutzt wird.
"""

# Wenn `render = False`, wird das Spiel nicht visuell gerendert.
# Dies ist nützlich, wenn man z. B. den Algorithmus schneller simulieren möchte (ohne UI).
# Wenn `render = True`, wird das Spiel wie gewohnt grafisch dargestellt.
render = True

# Steuerung der Clock:
# Wenn `use_clock = False`, wird die Clock-Funktion deaktiviert, und das Spiel läuft so schnell wie möglich.
# Wenn `use_clock = True`, reguliert die Clock die Geschwindigkeit des Spiels auf `SPEED`.
use_clock = False

debug_mode = True

use_heat_map = False  # Heatmap an/aus-Schalter

START_X = 5 * BLOCK_SIZE  # Fester Startpunkt (X-Koordinate)
START_Y = 5 * BLOCK_SIZE  # Fester Startpunkt (Y-Koordinate)

Point = namedtuple('Point', 'x, y')