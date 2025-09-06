# AI Catch Game

Ein studentisches KI-Projekt basierend auf dem "Snake Game AI"-Projekt von [patrickloeber](https://github.com/patrickloeber/snake-ai-pytorch). Ziel des Spiels ist es, einem KI-Agenten beizubringen, sich auf einem Spielfeld mit oder ohne Hindernisse optimal zu bewegen, um die Punktzahl zu maximieren und Kollisionen zu vermeiden.



## Voraussetzungen

- Eine IDE oder ein Framework, das die Ausführung von Python-Dateien (.py) unterstützt
- Installierte Abhängigkeiten (wir empfehlen die Nutzung einer [virtuellen Umgebung](https://learn.arcade.academy/de/latest/chapters/xx_venv_setup/):
  - pygame
  - torch
  - heapq
  - matplotlib
  - seaborn
  - numpy

## Installation & Nutzung

1. Repository klonen oder herunterladen:
   ```bash
   git clone https://github.com/huber2511/AI-Catch-Game-mapped-Path-Fider/
   cd AI-Catch-Game-mapped-Path-Fider
   ```
2. Virtuelle Umgebung erstellen und aktivieren (empfohlen):
   ```bash
   python -m venv venv
   source venv/bin/activate  # macOS/Linux
   venv\Scripts\activate  # Windows
   ```
3. Abhängigkeiten installieren:
   ```bash
   pip install -r requirements.txt
   ```
4. Das Spiel starten:
   ```bash
   python agent.py
   ```

## Spielmechanik

Das Spiel "AI Catch Game" basiert auf einer einfachen Umgebung, in der der Agent versucht, Essen zu fangen, während er Hindernissen ausweicht. 
- Der Agent bewegt sich innerhalb eines Spielfelds und nutzt eine Heatmap zur Analyse seiner Bewegungen.
- Ein Belohnungssystem sorgt dafür, dass der Agent für sinnvolle Aktionen belohnt und für ineffiziente Bewegungen bestraft wird.
- Das Spiel endet, wenn der Agent mit einer Wand oder einem Hindernis kollidiert oder eine maximale Anzahl von Spielschritten überschritten wird.

## Künstliche Intelligenz

Der Agent wird durch ein neuronales Netz gesteuert, das mit Q-Learning trainiert wird:
- **Neuronales Netz:** Ein einfaches zweischichtiges Modell (`Linear_QNet`) mit ReLU-Aktivierung.
- **Trainingsmechanismus:** 
  - Erfahrungsspeicherung (Replay Memory) mit `deque`
  - Batch-Training mit `QTrainer`
  - Exploration vs. Exploitation durch eine variable Epsilon-Strategie
- **Belohnungssystem:** 
  - Belohnung für das Erreichen des Ziels
  - Strafen für Kollisionen und ineffiziente Bewegungen

