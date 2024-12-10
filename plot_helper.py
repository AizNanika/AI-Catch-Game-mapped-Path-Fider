import matplotlib.pyplot as plt


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
    plt.pause(0.1)
