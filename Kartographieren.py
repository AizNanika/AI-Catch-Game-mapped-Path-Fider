import matplotlib.pyplot as plt
import matplotlib.cm as cm
from config import WIDTH, HEIGHT  # Import WIDTH and HEIGHT from config.py

plt.ion()  # Enable interactive mode

# Global variables for the figure and axes
global_fig, global_ax = None, None

def aktualisiere_pfad_historie(pfad_historie, neuer_pfad):
    """
    Adds a new path to the history.

    Args:
        pfad_historie (list): List of previous paths.
        neuer_pfad (list): List of coordinates (x, y) forming the new path.
    """
    pfad_historie.append(neuer_pfad)

def initialisiere_karte(fenster_breite, fenster_hoehe):
    """
    Initializes the global figure and axes for visualization.

    Args:
        fenster_breite (int): Width of the window.
        fenster_hoehe (int): Height of the window.
    """
    global global_fig, global_ax
    if global_fig is None or global_ax is None:
        global_fig, global_ax = plt.subplots()
        global_ax.set_aspect('equal')  # Keep aspect ratio of axes equal
        global_ax.set_xlim(0, fenster_breite)
        global_ax.set_ylim(0, fenster_hoehe)
        plt.title("Path Map")

def visualisiere_pfad(pfad_historie):
    """
    Visualizes the paths in a single window using matplotlib.

    Args:
        pfad_historie (list): List of previous paths.
    """
    global global_fig, global_ax

    # Initialize the window if it does not exist
    initialisiere_karte(WIDTH, HEIGHT)  # Use WIDTH and HEIGHT from config.py

    # Clear old contents
    global_ax.clear()
    global_ax.set_aspect('equal')
    global_ax.set_xlim(0, WIDTH)  # Use WIDTH from config.py
    global_ax.set_ylim(0, HEIGHT)  # Use HEIGHT from config.py

    # Color palette for the heatmap
    farben = cm.get_cmap('Reds', 100)  # 100 shades of red

    for pfad in pfad_historie:
        x = [punkt[0] for punkt in pfad]
        y = [punkt[1] for punkt in pfad]
        global_ax.plot(x, y, color='black', linewidth=2)  # Path in black

    # Create heatmap
    alle_punkte = [punkt for pfad in pfad_historie for punkt in pfad]
    for punkt in alle_punkte:
        haeufigkeit = alle_punkte.count(punkt)
        farbindex = min(haeufigkeit, 99)  # Map frequency to color index
        global_ax.scatter(punkt[0], punkt[1], color=farben(farbindex), s=50)  # Draw point

    plt.pause(0.001)  # Short pause for updating