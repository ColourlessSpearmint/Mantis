import torch
import torch.optim as optim
import torch.nn as nn
from model import MantisNN
from replay_buffer import ReplayBuffer
import random

import env

# Hyperparameters
BATCH_SIZE = 32
LR = 1e-3
GAMMA = 0.99
EPSILON_START = 1.0
EPSILON_END = 0.05
EPSILON_DECAY = 0.995
REPLAY_CAPACITY = 10000
EPISODES = 1000

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Initialize the model, optimizer, and replay buffer
model = MantisNN().to(device)
optimizer = optim.Adam(model.parameters(), lr=LR)
loss_fn = nn.MSELoss()
replay_buffer = ReplayBuffer(REPLAY_CAPACITY)

def epsilon_greedy_policy(state, epsilon):
    if random.random() < epsilon:
        # Random action
        return random.randint(0, 3)
    else:
        # Choose action with max Q-value
        state_tensor = torch.FloatTensor(state).unsqueeze(0).to(device)
        q_values = model(state_tensor)
        return torch.argmax(q_values, dim=1).item()

def train_step(batch):
    states, actions, rewards, next_states = zip(*batch)
    states = torch.FloatTensor(states).to(device)
    actions = torch.LongTensor(actions).to(device)
    rewards = torch.FloatTensor(rewards).to(device)
    next_states = torch.FloatTensor(next_states).to(device)

    q_values = model(states)
    next_q_values = model(next_states)
    
    # Compute the target Q-value
    max_next_q_values = next_q_values.max(dim=1)[0]
    target_q_values = rewards + GAMMA * max_next_q_values

    # Get the Q-value for the taken action
    current_q_values = q_values.gather(1, actions.unsqueeze(1)).squeeze(1)
    
    # Compute the loss
    loss = loss_fn(current_q_values, target_q_values)

    # Optimize the model
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()

def train():
    epsilon = EPSILON_START
    game = env.mantis()  # Assuming your environment is initialized like this
    for episode in range(EPISODES):
        game.reset()
        state = game.get_inputs()  # Get initial state
        done = False
        while not done:
            action = epsilon_greedy_policy(state, epsilon)
            next_state, done = game.take_action(action)  # Take action, reward is handled externally
            
            # Here we handle the reward logic based on whether the game is done
            if done:
                if game.has_won():  # You can check the winning condition directly
                    reward = 1  # Positive reward for winning
                else:
                    reward = -1  # Negative reward for losing

            replay_buffer.add((state, action, reward, next_state))
            
            # Training step
            if replay_buffer.size() >= BATCH_SIZE:
                batch = replay_buffer.sample(BATCH_SIZE)
                train_step(batch)

            state = next_state

        # Decay epsilon
        epsilon = max(EPSILON_END, epsilon * EPSILON_DECAY)
        print(f"Episode {episode}, Epsilon {epsilon}")


if __name__ == '__main__':
    train()
