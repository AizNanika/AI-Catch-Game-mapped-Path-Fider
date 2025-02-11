import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns  # Für schönere Heatmaps
from obstacles import obstacles  # Hindernisse importieren
from config import BLOCK_SIZE  # Blockgröße importieren

HEATMAP_FOLDER = "heatmaps"
if not os.path.exists(HEATMAP_FOLDER):
    os.makedirs(HEATMAP_FOLDER)


def save_heatmap(heatmap, game_number, end_pos, food_pos):
    """
    Speichert die Heatmap als Bild mit besserer Farbskala, Transparenz und sichtbaren Hindernissen.
    """
    plt.figure(figsize=(6, 6))

    # Logarithmische Skalierung für bessere Sichtbarkeit kleiner Werte
    norm_heatmap = np.log1p(heatmap)

    # Hintergrund auf ein helles Grau setzen, um Kontrast zu verbessern
    plt.gca().set_facecolor('#ffffff')

    # Heatmap mit verbessertem Farbverlauf (Alternativen: 'coolwarm', 'magma')
    ax = sns.heatmap(norm_heatmap.T, cmap='inferno', cbar=True, square=True, linewidths=0.0,
                     linecolor='white', vmin=0, vmax=np.percentile(norm_heatmap, 99))

    # Zeichne Hindernisse mit Transparenz
    for obstacle in obstacles:
        x_start = obstacle["x"] // BLOCK_SIZE
        y_start = obstacle["y"] // BLOCK_SIZE
        width = obstacle["width"] // BLOCK_SIZE
        height = obstacle["height"] // BLOCK_SIZE

        rect = plt.Rectangle((x_start, y_start), width, height, color='#646464', alpha=0.5)  # 50% Transparenz
        ax.add_patch(rect)

    # Markiere die Endposition (gelb)
    end_marker = plt.scatter(end_pos[0] + 0.5, end_pos[1] + 0.5, color='yellow', marker='o', s=80, label="Ende")

    # Markiere die Essensposition (rot)
    food_marker = plt.scatter(food_pos[0] + 0.5, food_pos[1] + 0.5, color='red', marker='x', s=100, label="Essen")

    plt.title(f"Heatmap - Spiel {game_number}")

    # Legende verbessern
    plt.legend(handles=[end_marker, food_marker,
                        plt.Line2D([0], [0], color='#404040', lw=4, label="Hindernis")])

    # Speichern der Datei mit hoher Auflösung
    filename = os.path.join(HEATMAP_FOLDER, f"heatmap_{game_number}.png")
    plt.savefig(filename, dpi=600, bbox_inches='tight')  # Höhere DPI für schärfere Darstellung
    plt.close()

    # Behalte nur die letzten 5 Heatmaps
    files = sorted(os.listdir(HEATMAP_FOLDER), key=lambda x: os.path.getctime(os.path.join(HEATMAP_FOLDER, x)),
                   reverse=True)
    while len(files) > 5:
        os.remove(os.path.join(HEATMAP_FOLDER, files.pop()))



def plot(scores):
    """
    Plottet die Scores und den Durchschnitt über alle Spiele.
    """
    x = list(range(1, len(scores) + 1))  # Spiele
    cumulative_mean = [sum(scores[:i + 1]) / (i + 1) for i in range(len(scores))]  # Durchschnitts-Scores

    plt.clf()
    plt.plot(3, scores, marker="o", label="Scores")
    plt.plot(x, cumulative_mean, linestyle="--", color="orange", label="Durchschnittlicher Score")
    plt.title("Scores und Durchschnittlicher Score über die Spiele")
    plt.xlabel("Spiele")
    plt.ylabel("Scores")
    plt.legend()
    plt.grid(True)
    plt.show(block=False)
    plt.pause(0.1)

def plot_losses(scores, losses):
    """
    Plottet Scores und Loss-Werte in zwei Diagrammen.
    """
    x = list(range(1, len(scores) + 1))

    plt.figure(figsize=(12, 5))

    # Score-Plot
    plt.subplot(1, 2, 1)
    plt.plot(x, scores, marker="o", label="Scores")
    plt.plot(x, [sum(scores[:i+1]) / (i+1) for i in range(len(scores))], linestyle="--", color="orange", label="Durchschnittlicher Score")
    plt.title("Scores über die Spiele")
    plt.xlabel("Spiele")
    plt.ylabel("Score")
    plt.legend()
    plt.grid(True)

    # Loss-Plot
    plt.subplot(1, 2, 2)
    plt.plot(x, losses, marker="o", color="red", label="Loss")
    plt.title("Loss-Verlauf")
    plt.xlabel("Spiele")
    plt.ylabel("Loss")
    plt.legend()
    plt.grid(True)

    plt.show(block=False)
    plt.pause(0.1)


def plot_steps(agent_steps, optimal_steps, deviations):
    import matplotlib.pyplot as plt

    x = list(range(1, len(agent_steps) + 1))

    plt.figure(figsize=(12, 5))

    # Plot für Agenten-Schritte vs. optimale A*-Schritte
    plt.subplot(1, 2, 1)
    plt.plot(x, agent_steps, marker="o", label="Agent Steps")
    plt.plot(x, optimal_steps, marker="x", label="Optimal Steps (A*)")
    plt.xlabel("Spiel")
    plt.ylabel("Anzahl durchschnittlicher Schritte")
    plt.title("Agenten-Schritte vs. Optimale A*-Schritte")
    plt.legend()
    plt.grid(True)

    # Plot für die Abweichung
    plt.subplot(1, 2, 2)
    plt.plot(x, deviations, marker="d", color="red", label="Abweichung")
    plt.xlabel("Spiel")
    plt.ylabel("Differenz in Schritten")
    plt.title("Abweichung zum optimalen A*-Weg")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()
