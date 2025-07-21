import os
import random
import pickle
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
import numpy as np

# --- Helper functions (remains the same) ---
def get_topic_category(topic):
    # ...
    return "General"

def get_youtube_comments_sentiment(video_id):
    # ...
    return 0.0

# --- Deep Q-Network (DQN) Implementation ---
class DQN(nn.Module):
    def __init__(self, n_states, n_actions):
        super(DQN, self).__init__()
        self.layer1 = nn.Linear(n_states, 128)
        self.layer2 = nn.Linear(128, 128)
        self.layer3 = nn.Linear(128, n_actions)

    def forward(self, x):
        x = F.relu(self.layer1(x))
        x = F.relu(self.layer2(x))
        return self.layer3(x)

class ReplayMemory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.memory = []
        self.position = 0

    def push(self, *args):
        if len(self.memory) < self.capacity:
            self.memory.append(None)
        self.memory[self.position] = tuple(args)
        self.position = (self.position + 1) % self.capacity

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)

class DQNAgent:
    def __init__(self, state_dim, action_dim, model_path='dqn_model.pth', capacity=10000, lr=1e-4, gamma=0.9, epsilon=0.9, batch_size=128):
        self.state_dim = state_dim
        self.action_dim = action_dim
        self.model_path = os.path.join("zero_touch_mikrotik", "data", model_path)

        self.policy_net = DQN(state_dim, action_dim)
        self.target_net = DQN(state_dim, action_dim)
        if os.path.exists(self.model_path):
            self.policy_net.load_state_dict(torch.load(self.model_path))
        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.target_net.eval()

        self.optimizer = optim.Adam(self.policy_net.parameters(), lr=lr)
        self.memory = ReplayMemory(capacity)
        self.gamma = gamma
        self.epsilon = epsilon
        self.batch_size = batch_size

    def select_action(self, state):
        if random.random() > self.epsilon:
            with torch.no_grad():
                return self.policy_net(state).max(1)[1].view(1, 1)
        else:
            return torch.tensor([[random.randrange(self.action_dim)]], dtype=torch.long)

    def optimize_model(self):
        if len(self.memory) < self.batch_size:
            return

        transitions = self.memory.sample(self.batch_size)
        batch = tuple(zip(*transitions))

        state_batch = torch.cat(batch[0])
        action_batch = torch.cat(batch[1])
        reward_batch = torch.cat(batch[2])

        state_action_values = self.policy_net(state_batch).gather(1, action_batch)

        # For now, we don't have a next_state, so the expected value is just the reward
        expected_state_action_values = reward_batch

        loss = F.smooth_l1_loss(state_action_values, expected_state_action_values.unsqueeze(1))

        self.optimizer.zero_grad()
        loss.backward()
        for param in self.policy_net.parameters():
            param.grad.data.clamp_(-1, 1)
        self.optimizer.step()

    def save_model(self):
        torch.save(self.policy_net.state_dict(), self.model_path)

# --- Global Mappings for State and Action ---
# This is crucial for converting categorical data to numbers
TOPIC_CATEGORIES = {"General": 0, "Firewall": 1, "VPN": 2, "Routing": 3}
LENGTH_CATEGORIES = {"Short": 0, "Long": 1}
# Let's define a fixed set of possible actions (topics) for simplicity
POSSIBLE_TOPICS = ["MikroTik Firewall Rules", "MikroTik VPN Setup", "MikroTik OSPF Routing", "MikroTik Basic Setup", "MikroTik VLANs", "MikroTik QoS"]
ACTION_MAP = {topic: i for i, topic in enumerate(POSSIBLE_TOPICS)}
ACTION_MAP_REV = {i: topic for topic, i in ACTION_MAP.items()}

def state_to_tensor(category, length):
    cat_idx = TOPIC_CATEGORIES.get(category, 0)
    len_idx = LENGTH_CATEGORIES.get(length, 0)
    # Create a one-hot encoded vector
    state = np.zeros(len(TOPIC_CATEGORIES) + len(LENGTH_CATEGORIES))
    state[cat_idx] = 1
    state[len(TOPIC_CATEGORIES) + len_idx] = 1
    return torch.FloatTensor(state).unsqueeze(0)

def analyze_feedback(topic, video_duration_sec, youtube_video_id):
    """
    Analyzes feedback and updates the DQN model.
    """
    print("Analyzing feedback with DQN...")

    # --- Initialize Agent ---
    state_dim = len(TOPIC_CATEGORIES) + len(LENGTH_CATEGORIES)
    action_dim = len(POSSIBLE_TOPICS)
    agent = DQNAgent(state_dim, action_dim)

    # --- Get Feedback and Calculate Reward ---
    feedback = { "ctr": round(random.uniform(0.01, 0.15), 3), "watch_time_avg_sec": random.randint(30, 400) }
    sentiment_score = get_youtube_comments_sentiment(youtube_video_id)
    reward = (feedback["ctr"] * 100) + (feedback["watch_time_avg_sec"] / 10) + (sentiment_score * 20)

    # --- Prepare Tensors for Memory ---
    category = get_topic_category(topic)
    length = "Short" if video_duration_sec < 300 else "Long"
    state = state_to_tensor(category, length)

    action_idx = ACTION_MAP.get(topic)
    if action_idx is None:
        print(f"Warning: Topic '{topic}' not in pre-defined action map. Skipping learning for this step.")
        return feedback

    action = torch.tensor([[action_idx]], dtype=torch.long)
    reward_tensor = torch.tensor([reward], dtype=torch.float)

    # --- Store experience and optimize ---
    agent.memory.push(state, action, reward_tensor)
    agent.optimize_model()
    agent.save_model()

    print(f"DQN model updated and saved.")
    return feedback
