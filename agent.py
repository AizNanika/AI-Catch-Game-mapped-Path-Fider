import torch  # Hauptbibliothek für das neuronale Netz
import random  # Bibliothek für die zufälligen bewegungen, z.B. für Explorations-Phase
import numpy as np  # Für dem umgang mit arrays
from collections import deque  # Schneller Speicher (Queue) für Übergangszustände im Replay-Memory

# Hilfsklassen aus dem Projekt
from environment import CatchGameEnv, Direction, Point
from model import Linear_QNet, QTrainer
from plot_helper import plot, plot_steps
from plot_helper import plot_losses as plot_loss_function

MAX_MEMORY = 100_000  # Maximale Anzahl an gespeicherten Spielzuständen im Replay-Memory
BATCH_SIZE = 1000  # Anzahl an Spielzuständen für das Batch-Training
LR = 0.001  # Lernrate für den Optimierungsalgorithmus


# Agenten Klasse
class Agent:

    # Konstruktor
    def __init__(self):
        self.n_games = 0  # Anzahl der gesamten Spiele, mit 0
        self.epsilon = 0  # randomness,n mit 0
        self.gamma = 0.9  # discount rate, mit 0.9
        self.memory = deque(maxlen=MAX_MEMORY)  # popleft()
        self.model = Linear_QNet(19, 256, 4)  # Eingabegröße auf 19 erhöht
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, env):
        head = env.head
        point_l = Point(head.x - env.get_block_size(), head.y)
        point_r = Point(head.x + env.get_block_size(), head.y)
        point_u = Point(head.x, head.y - env.get_block_size())
        point_d = Point(head.x, head.y + env.get_block_size())

        dir_l = env.direction == Direction.LEFT
        dir_r = env.direction == Direction.RIGHT
        dir_u = env.direction == Direction.UP
        dir_d = env.direction == Direction.DOWN

        state = [
            # Gefahr geradeaus (Wand oder Hindernis)
            (dir_r and env.is_collision(point_r)) or
            (dir_l and env.is_collision(point_l)) or
            (dir_u and env.is_collision(point_u)) or
            (dir_d and env.is_collision(point_d)),

            # Gefahr rechts (Wand oder Hindernis)
            (dir_u and env.is_collision(point_r)) or
            (dir_d and env.is_collision(point_l)) or
            (dir_l and env.is_collision(point_u)) or
            (dir_r and env.is_collision(point_d)),

            # Gefahr links (Wand oder Hindernis)
            (dir_d and env.is_collision(point_r)) or
            (dir_u and env.is_collision(point_l)) or
            (dir_r and env.is_collision(point_u)) or
            (dir_l and env.is_collision(point_d)),

            # Bewegungsrichtung
            dir_l,
            dir_r,
            dir_u,
            dir_d,

            # Position des Essens relativ zum Kopf
            env.food.x < env.head.x,  # Essen links
            env.food.x > env.head.x,  # Essen rechts
            env.food.y < env.head.y,  # Essen oben
            env.food.y > env.head.y,  # Essen unten

            # Hindernisse direkt vor dem Agenten
            env.is_collision(point_r),  # Hindernis rechts
            env.is_collision(point_l),  # Hindernis links
            env.is_collision(point_u),  # Hindernis oben
            env.is_collision(point_d),  # Hindernis unten

            # Freie Wege erkennen
            not env.is_collision(point_r),  # Freier Weg nach rechts
            not env.is_collision(point_l),  # Freier Weg nach links
            not env.is_collision(point_u),  # Freier Weg nach oben
            not env.is_collision(point_d)  # Freier Weg nach unten
        ]

        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))  # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE)  # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        loss = self.trainer.train_step(states, actions, rewards, next_states, dones)
        return loss

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.n_games
        final_move = [0, 0, 0, 0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 3)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move


plot_scores = []
plot_losses = []
total_score = 0
record = 0

agent_steps_list = []
optimal_steps_list = []
deviation_list = []



def train():
    global plot_scores, plot_losses, total_score, record
    agent = Agent()
    env = CatchGameEnv()

    while True:
        state_old = agent.get_state(env)
        final_move = agent.get_action(state_old)
        reward, done, score, steps = env.play_step(final_move)
        state_new = agent.get_state(env)

        # Bestrafung für unnötige Bewegungen
        if state_old.tolist() == state_new.tolist():
            reward -= 0.1

        agent.train_short_memory(state_old, final_move, reward, state_new, done)
        agent.remember(state_old, final_move, reward, state_new, done)

        steps += 1

        if done:
            env.reset()
            agent.n_games += 1
            loss = agent.train_long_memory()  # Loss speichern

            if score > record:
                record = score
                agent.model.save()

            print(
                f"Game {agent.n_games} | Score: {score} | Record: {record} | Loss: {loss:.4f} | Eps: {agent.epsilon} | AvSt: {steps // (score + 1)}")

            plot_scores.append(score)
            plot_losses.append(loss)
            optimal_steps = env.get_optimal_steps()  # Diese Methode musst du in CatchGameEnv integrieren
            agent_steps_list.append(steps // (score + 1))
            optimal_steps_list.append(optimal_steps)
            deviation_list.append(steps - optimal_steps)

            if agent.n_games % 10 == 0:
                plot_steps(agent_steps_list, optimal_steps_list, deviation_list)
                plot_loss_function(plot_scores, plot_losses)


if __name__ == '__main__':
    train()
