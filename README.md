# AI Catch Game

Ein studentisches KI-Projekt basierend auf dem "Snake Game AI"-Projekt von [patrickloeber](https://github.com/patrickloeber/snake-ai-pytorch). Ziel des Spiels ist es, einem KI-Agenten beizubringen, sich auf einem Spielfeld mit oder ohne Hindernisse optimal zu bewegen, um die Punktzahl zu maximieren und Kollisionen zu vermeiden.

![Gameplay Screenshot](/path/to/image.png)  
*(Ersetze dies mit einem tatsächlichen Bild deines Spiels)*

## Voraussetzungen
- Eine IDE oder ein Framework, das die Ausführung von Python-Dateien (.py) unterstützt
- Installierte Abhängigkeiten (wir empfehlen die Nutzung einer [virtuellen Umgebung](https://learn.arcade.academy/de/latest/chapters/xx_venv_setup/)):
  - pygame
  - torch
  - heapq
  - matplotlib
  - seaborn
  - numpy

## Installation & Nutzung
1. Repository klonen oder herunterladen:
   ```bash
   git clone https://github.com/dein-repo-link.git
   cd AI-Catch-Game
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
