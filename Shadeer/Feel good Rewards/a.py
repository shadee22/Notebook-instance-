import gym
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam

# Create the environment
env = gym.make('CartPole-v1')

# Define the DQN model
model = Sequential()
model.add(Dense(24, input_shape=env.observation_space.shape, activation='relu'))
model.add(Dense(24, activation='relu'))
model.add(Dense(env.action_space.n, activation='linear'))
model.compile(loss='mse', optimizer=Adam(learning_rate=0.001))

# Define the RL training parameters
num_episodes = 1000
max_steps_per_episode = 1000
epsilon = 1.0
epsilon_decay = 0.995
min_epsilon = 0.01
batch_size = 32
gamma = 0.99

# Train the RL model
for episode in range(num_episodes):
    state = env.reset()
    done = False
    total_reward = 0

    for step in range(max_steps_per_episode):
        # Choose an action using epsilon-greedy policy
        if np.random.rand() <= epsilon:
            action = env.action_space.sample()
        else:
            q_values = model.predict(np.expand_dims(state, axis=0))
            action = np.argmax(q_values[0])

        # Perform the action and observe the next state and reward
        next_state, reward, done, _ = env.step(int(action))

        # Update the Q-value using the Bellman equation
        target = reward + gamma * np.amax(model.predict(np.expand_dims(next_state, axis=0))[0])
        q_values = model.predict(np.expand_dims(state, axis=0))
        q_values[0][action] = target

        # Train the model on a batch of experiences
        model.fit(np.expand_dims(state, axis=0), q_values, verbose=0, batch_size=batch_size)

        state = next_state
        total_reward += reward

        if done:
            break

    # Decay epsilon
    if epsilon > min_epsilon:
        epsilon *= epsilon_decay

    # Print the episode results
    print(f"Episode {episode + 1}: Total Reward = {total_reward}")

# Test the RL model
state = env.reset()
done = False
total_reward = 0

while not done:
    env.render()
    q_values = model.predict(np.expand_dims(state, axis=0))
    action = np.argmax(q_values[0])
    state, reward, done, _ = env.step(int(action))
    total_reward += reward

print(f"Test Result: Total Reward = {total_reward}")

# Close the environment
env.close()

