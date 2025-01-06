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
EPISODES = 20000
WIN_RATE_THRESHOLD = 0.6  # New hyperparameter: required win rate to change state
WIN_RATE_WINDOW = 30      # New hyperparameter: number of episodes to calculate win rate

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
    game = env.mantis()
    total_wins = 0
    cached_game = None
    recent_wins = []
    
    for episode in range(EPISODES):
        # Generate new starting state if needed
        if cached_game is None or (len(recent_wins) >= WIN_RATE_WINDOW and sum(recent_wins) / WIN_RATE_WINDOW >= WIN_RATE_THRESHOLD):
            game.reset()  # Reset to a new random state
            cached_game = game.game  # Cache the new state
            recent_wins = []  # Reset recent wins tracker
        else:
            game.game = cached_game  # Restore cached state
            game.game.deck_index = 0
            
        state = game.get_inputs()  # Get the initial game state
        done = False
        temp_buffer = []
        
        while not done:
            action = epsilon_greedy_policy(state, epsilon)
            next_state, done = game.take_action(action)
            
            # Add experience to the replay buffer
            temp_buffer.append((state, action, 0, next_state))

            state = next_state

        # After the game ends, assign reward based on whether the agent won
        if game.has_won():
            reward = 1  # Positive reward for winning
            total_wins += 1  # Increment win counter
            recent_wins.append(1)  # Track win
        else:
            reward = -1  # Negative reward for losing
            recent_wins.append(0)  # Track loss

        # Maintain the size of recent_wins to be within WIN_RATE_WINDOW
        if len(recent_wins) > WIN_RATE_WINDOW:
            recent_wins.pop(0)

        # Now update the experiences in the replay buffer with the final reward
        for experience in temp_buffer:
            state, action, _, next_state = experience
            replay_buffer.add((state, action, reward, next_state))

        # Training step (after the episode is completed)
        if replay_buffer.size() >= BATCH_SIZE:
            batch = replay_buffer.sample(BATCH_SIZE)
            train_step(batch)

        # Decay epsilon (decreasing randomness over time)
        epsilon = max(EPSILON_END, epsilon * EPSILON_DECAY)
        
        # Displaying some analytics
        win_rate = total_wins / (episode + 1)
        print(f"Episode {episode+1}/{EPISODES}, Wins: {total_wins}, Epsilon {epsilon:.4f}, Win Rate: {win_rate:.4f}, Recent Win Rate: {sum(recent_wins) / len(recent_wins):.4f}")

    print(f"Training complete. Model achieved {total_wins} wins out of {EPISODES} episodes.")

if __name__ == '__main__':
    train()
