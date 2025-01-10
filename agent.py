import torch # Hauptbibliothek für das neuronale Netz
import random # Bibliothek für die zufälligen bewegungen, z.B. für Explorations-Phase
import numpy as np # Für dem umgang mit arrays
from collections import deque # Schneller Speicher (Queue) für Übergangszustände im Replay-Memory
import pygame

# Hilfsklassen aus dem Projekt
from environment import CatchGameEnv, Direction, Point
from model import Linear_QNet, QTrainer
from plot_helper import plot
from Kartographieren import visualisiere_pfad, aktualisiere_pfad_historie

MAX_MEMORY = 100_000 # Maximale Anzahl an gespeicherten Spielzuständen im Replay-Memory
BATCH_SIZE = 1000 # Anzahl an Spielzuständen für das Batch-Training
LR = 0.001 # Lernrate für den Optimierungsalgorithmus

# Agenten Klasse
class Agent:

    #Konstruktor
    def __init__(self):
        self.n_games = 0 # Anzahl der gesamten Spiele, mit 0
        self.epsilon = 0 # randomness,n mit 0
        self.gamma = 0.9 # discount rate, mit 0.9
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.model = Linear_QNet(11, 256, 4)
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
            # Danger straight
            (dir_r and env.is_collision(point_r)) or
            (dir_l and env.is_collision(point_l)) or
            (dir_u and env.is_collision(point_u)) or
            (dir_d and env.is_collision(point_d)),

            # Danger right
            (dir_u and env.is_collision(point_r)) or
            (dir_d and env.is_collision(point_l)) or
            (dir_l and env.is_collision(point_u)) or
            (dir_r and env.is_collision(point_d)),

            # Danger left
            (dir_d and env.is_collision(point_r)) or
            (dir_u and env.is_collision(point_l)) or
            (dir_r and env.is_collision(point_u)) or
            (dir_l and env.is_collision(point_d)),
            
            # Move direction
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            
            # Food location 
            env.food.x < env.head.x,  # food left
            env.food.x > env.head.x,  # food right
            env.food.y < env.head.y,  # food up
            env.food.y > env.head.y  # food down
            ]

        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) # popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        #for state, action, reward, next_state, done in mini_sample:
        #    self.trainer.train_step(state, action, reward, next_state, done)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.n_games
        final_move = [0,0,0,0]
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 3)
            final_move[move] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move

pfad_historie = []  # initialize path history

def train():
    plot_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    env = CatchGameEnv()

    neuer_pfad = []  # list of current path
    anzahl_durchlaeufe = 0  # Counter of runs

    while True:
        # get old state
        state_old = agent.get_state(env)

        neuer_pfad.append((env.head.x, env.head.y))  # Position zu neuem Pfad hinzufügen

        # get move
        final_move = agent.get_action(state_old)

        # perform move and get new state
        reward, done, score = env.play_step(final_move)
        state_new = agent.get_state(env)

        # train short memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)

        # remember
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            # train long memory, plot result
            env.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            print('Game', agent.n_games, 'Score', score, 'Record:', record,'Reward', reward , 'Eps:', agent.epsilon)

            plot_scores.append(score)
            total_score += score
            plot(plot_scores)

            aktualisiere_pfad_historie(pfad_historie, neuer_pfad)  # Update the history
            anzahl_durchlaeufe += 1  # Count the run

            # Update visualization every 10 runs
            if anzahl_durchlaeufe % 10 == 0:  
                visualisiere_pfad(pfad_historie)

            neuer_pfad = []  # Start a new path for the next game

if __name__ == '__main__':
    train()