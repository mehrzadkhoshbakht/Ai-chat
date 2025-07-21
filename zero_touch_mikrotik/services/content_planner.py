import random
import os
import torch
from services.ai_model import DQN, state_to_tensor, TOPIC_CATEGORIES, LENGTH_CATEGORIES, ACTION_MAP_REV, STATE_DIM, ACTION_DIM

def plan_content(trending_topics):
    """
    Selects a topic using the centralized Deep Q-Network.
    """
    print("Planning content using centralized DQN...")

    # Load the trained model
    model_path = os.path.join("zero_touch_mikrotik", "data", "dqn_model.pth")
    policy_net = DQN(STATE_DIM, ACTION_DIM)
    if os.path.exists(model_path):
        policy_net.load_state_dict(torch.load(model_path))
    policy_net.eval()

    # Decide on video length and topic category
    length_category = random.choice(list(LENGTH_CATEGORIES.keys()))
    topic_category = random.choice(list(TOPIC_CATEGORIES.keys()))
    estimated_duration = 180 if length_category == "Short" else 600

    state = state_to_tensor(topic_category, length_category)

    # Epsilon-greedy selection for planning
    epsilon = 0.1
    if random.random() < epsilon:
        print("Exploring a random action (topic)...")
        action_idx = random.randrange(ACTION_DIM)
    else:
        print(f"Choosing best action for state ({topic_category}, {length_category})...")
        with torch.no_grad():
            action_idx = policy_net(state).max(1)[1].item()

    selected_topic = ACTION_MAP_REV[action_idx]

    # A simple way to still incorporate trends
    if trending_topics and selected_topic not in trending_topics and random.random() < 0.5:
        print(f"Overriding DQN's choice ('{selected_topic}') with a trending topic.")
        selected_topic = random.choice(trending_topics)

    print(f"Selected topic: {selected_topic} (for a {length_category} video)")
    return selected_topic, estimated_duration
