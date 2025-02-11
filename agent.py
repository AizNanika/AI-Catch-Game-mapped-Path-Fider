"""
Implementiert den KI-Agenten mit Q-Learning.
"""
import directions
import torch
import random
import numpy as np
from collections import deque
from environment import CatchGameEnv
from model import Linear_QNet, QTrainer
from config import Point


class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0  # Steuerung der Exploration
        self.gamma = 0.9  # Discount-Faktor
        self.memory = deque(maxlen=100_000)
        self.model = Linear_QNet(19, 256, 4)
        self.trainer = QTrainer(self.model, lr=0.001, gamma=self.gamma)

    def get_state(self, env):
        """Extrahiert den aktuellen Zustand aus der Umgebung."""
        head = env.head
        block_size = env.get_block_size()

        # Berechne benachbarte Punkte
        point_l = Point(head.x - block_size, head.y)
        point_r = Point(head.x + block_size, head.y)
        point_u = Point(head.x, head.y - block_size)
        point_d = Point(head.x, head.y + block_size)

        # Aktuelle Richtung
        dir_l = env.direction == directions.Direction.LEFT
        dir_r = env.direction == directions.Direction.RIGHT
        dir_u = env.direction == directions.Direction.UP
        dir_d = env.direction == directions.Direction.DOWN

        # Erstelle State-Vektor
        state = [
            # Gefahren erkennung
            (dir_r and env.is_collision(point_r)) or
            (dir_l and env.is_collision(point_l)) or
            (dir_u and env.is_collision(point_u)) or
            (dir_d and env.is_collision(point_d)),

            (dir_u and env.is_collision(point_r)) or
            (dir_d and env.is_collision(point_l)) or
            (dir_l and env.is_collision(point_u)) or
            (dir_r and env.is_collision(point_d)),

            (dir_d and env.is_collision(point_r)) or
            (dir_u and env.is_collision(point_l)) or
            (dir_r and env.is_collision(point_u)) or
            (dir_l and env.is_collision(point_d)),

            # Bewegungsrichtung
            dir_l, dir_r, dir_u, dir_d,

            # Position des Essens
            env.food.x < env.head.x,  # links
            env.food.x > env.head.x,  # rechts
            env.food.y < env.head.y,  # oben
            env.food.y > env.head.y,  # unten

            # Hindernisse
            env.is_collision(point_r),
            env.is_collision(point_l),
            env.is_collision(point_u),
            env.is_collision(point_d),

            # Freie Wege
            not env.is_collision(point_r),
            not env.is_collision(point_l),
            not env.is_collision(point_u),
            not env.is_collision(point_d)
        ]

        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        """Speichert eine Erfahrung im Replay-Memory."""
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        """Trainiert das Modell mit einer Batch aus dem Replay-Memory."""
        if len(self.memory) > 1000:
            mini_sample = random.sample(self.memory, 1000)
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        return self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        """Trainiert das Modell mit einer einzelnen Erfahrung."""
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        """Wählt eine Aktion basierend auf dem aktuellen Zustand."""
        self.epsilon = max(80 - self.n_games * 0.5, 0)
        final_move = [0, 0, 0, 0]

        if random.randint(0, 200) < self.epsilon:
            # Exploration: Zufällige Aktion
            move = random.randint(0, 3)
        else:
            # Exploitation: Beste Aktion laut Modell
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()

        final_move[move] = 1
        return final_move

def train():
    """Haupttrainingsfunktion."""
    plot_scores = []
    plot_losses = []
    agent = Agent()
    env = CatchGameEnv()

    while True:
        # Hole aktuellen Zustand
        state_old = agent.get_state(env)

        # Wähle und führe Aktion aus
        final_move = agent.get_action(state_old)
        reward, done, score, steps = env.play_step(final_move)
        state_new = agent.get_state(env)

        # Bestrafe unnötige Bewegungen
        if state_old.tolist() == state_new.tolist():
            reward -= 0.1

        # Trainiere Kurzzeit-Gedächtnis
        agent.train_short_memory(state_old, final_move, reward, state_new, done)
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # Trainiere Langzeit-Gedächtnis und reset Umgebung
            env.reset()
            agent.n_games += 1
            loss = agent.train_long_memory()

            if score > max(plot_scores, default=0):
                agent.model.save()

            print(f'Game {agent.n_games} | Score: {score} | Record: {max(plot_scores, default=0)} | Loss: {loss:.4f}')

            plot_scores.append(score)
            plot_losses.append(loss)

if __name__ == '__main__':
    train()