import random
import os
import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

# --- Re-using DQN and mappings from feedback_analytics ---
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

TOPIC_CATEGORIES = {"General": 0, "Firewall": 1, "VPN": 2, "Routing": 3}
LENGTH_CATEGORIES = {"Short": 0, "Long": 1}
POSSIBLE_TOPICS = ["MikroTik Firewall Rules", "MikroTik VPN Setup", "MikroTik OSPF Routing", "MikroTik Basic Setup", "MikroTik VLANs", "MikroTik QoS"]
ACTION_MAP_REV = {i: topic for i, topic in enumerate(POSSIBLE_TOPICS)}
STATE_DIM = len(TOPIC_CATEGORIES) + len(LENGTH_CATEGORIES)
ACTION_DIM = len(POSSIBLE_TOPICS)

def state_to_tensor(category, length):
    cat_idx = TOPIC_CATEGORIES.get(category, 0)
    len_idx = LENGTH_CATEGORIES.get(length, 0)
    state = np.zeros(STATE_DIM)
    state[cat_idx] = 1
    state[STATE_DIM - len(LENGTH_CATEGORIES) + len_idx] = 1 # Corrected indexing
    return torch.FloatTensor(state).unsqueeze(0)

def plan_content(trending_topics):
    """
    Selects a topic using the Deep Q-Network.
    """
    print("Planning content using DQN...")

    # Load the trained model
    model_path = os.path.join("zero_touch_mikrotik", "data", "dqn_model.pth")
    policy_net = DQN(STATE_DIM, ACTION_DIM)
    if os.path.exists(model_path):
        policy_net.load_state_dict(torch.load(model_path))
    policy_net.eval()

    # Decide on video length
    length_category = random.choice(["Short", "Long"])
    estimated_duration = 180 if length_category == "Short" else 600

    # For simplicity, let's try to pick a topic category as well
    # A more advanced approach would evaluate all possible states
    topic_category = random.choice(list(TOPIC_CATEGORIES.keys()))

    state = state_to_tensor(topic_category, length_category)

    # Epsilon-greedy selection
    epsilon = 0.1 # Lower epsilon during planning
    if random.random() < epsilon:
        print("Exploring a random action (topic)...")
        action_idx = random.randrange(ACTION_DIM)
        selected_topic = ACTION_MAP_REV[action_idx]
    else:
        print(f"Choosing best action for state ({topic_category}, {length_category})...")
        with torch.no_grad():
            action_idx = policy_net(state).max(1)[1].item()
            selected_topic = ACTION_MAP_REV[action_idx]

    # We still consider trending topics to add relevance
    # A simple way is to check if our selected topic is in trends, or pick a trending one
    if selected_topic not in trending_topics and trending_topics:
        if random.random() < 0.5: # 50% chance to override with a trending topic
            print(f"Overriding '{selected_topic}' with a trending topic.")
            selected_topic = random.choice(trending_topics)

    print(f"Selected topic: {selected_topic} (for a {length_category} video)")
    return selected_topic, estimated_duration
