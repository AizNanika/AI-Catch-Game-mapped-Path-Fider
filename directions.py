# directions.py
"""
Definiert die möglichen Bewegungsrichtungen im Spiel.
"""
from enum import Enum

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4