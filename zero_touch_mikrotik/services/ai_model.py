import os
import random
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
import torch.optim as optim

# --- Centralized AI Model Definitions ---

# 1. Global Mappings for State and Action
TOPIC_CATEGORIES = {"General": 0, "Firewall": 1, "VPN": 2, "Routing": 3}
LENGTH_CATEGORIES = {"Short": 0, "Long": 1}
POSSIBLE_TOPICS = ["MikroTik Firewall Rules", "MikroTik VPN Setup", "MikroTik OSPF Routing", "MikroTik Basic Setup", "MikroTik VLANs", "MikroTik QoS"]
ACTION_MAP = {topic: i for i, topic in enumerate(POSSIBLE_TOPICS)}
ACTION_MAP_REV = {i: topic for topic, i in ACTION_MAP.items()}
STATE_DIM = len(TOPIC_CATEGORIES) + len(LENGTH_CATEGORIES)
ACTION_DIM = len(POSSIBLE_TOPICS)

# 2. State Conversion Utility
def state_to_tensor(category, length):
    cat_idx = TOPIC_CATEGORIES.get(category, 0)
    len_idx = LENGTH_CATEGORIES.get(length, 0)
    state = np.zeros(STATE_DIM)
    state[cat_idx] = 1
    state[len(TOPIC_CATEGORIES) + len_idx] = 1
    return torch.FloatTensor(state).unsqueeze(0)

# 3. DQN Network Architecture
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

# 4. Replay Memory for Training
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

# 5. The DQNAgent Class
class DQNAgent:
    def __init__(self, model_path='dqn_model.pth', capacity=10000, lr=1e-4, gamma=0.9, epsilon=0.9, batch_size=128):
        self.state_dim = STATE_DIM
        self.action_dim = ACTION_DIM
        self.model_path = os.path.join("zero_touch_mikrotik", "data", model_path)

        self.policy_net = DQN(self.state_dim, self.action_dim)
        self.target_net = DQN(self.state_dim, self.action_dim)
        if os.path.exists(self.model_path):
            self.policy_net.load_state_dict(torch.load(self.model_path))
        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.target_net.eval()

        self.optimizer = optim.Adam(self.policy_net.parameters(), lr=lr)
        self.memory = ReplayMemory(capacity)
        self.gamma = gamma
        self.epsilon = epsilon
        self.batch_size = batch_size

    def select_action(self, state, use_epsilon=True):
        if use_epsilon and random.random() < self.epsilon:
            return torch.tensor([[random.randrange(self.action_dim)]], dtype=torch.long)
        else:
            with torch.no_grad():
                return self.policy_net(state).max(1)[1].view(1, 1)

    def optimize_model(self):
        if len(self.memory) < self.batch_size:
            return

        transitions = self.memory.sample(self.batch_size)
        batch = tuple(zip(*transitions))

        state_batch = torch.cat(batch[0])
        action_batch = torch.cat(batch[1])
        reward_batch = torch.cat(batch[2])

        state_action_values = self.policy_net(state_batch).gather(1, action_batch)
        expected_state_action_values = reward_batch.unsqueeze(1)

        loss = F.smooth_l1_loss(state_action_values, expected_state_action_values)

        self.optimizer.zero_grad()
        loss.backward()
        for param in self.policy_net.parameters():
            param.grad.data.clamp_(-1, 1)
        self.optimizer.step()

    def save_model(self):
        torch.save(self.policy_net.state_dict(), self.model_path)
