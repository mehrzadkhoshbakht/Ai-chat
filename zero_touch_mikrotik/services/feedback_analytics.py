import os
import random
import torch
from services.ai_model import DQNAgent, state_to_tensor, get_topic_category, ACTION_MAP

def get_youtube_comments_sentiment(video_id):
    # This function would remain the same, fetching comments and analyzing them
    # For brevity, we assume it's implemented elsewhere or remains as a placeholder
    print(f"Fetching sentiment for video {video_id} (placeholder)...")
    return random.uniform(-0.5, 0.5)

import json
from datetime import datetime

def log_performance_data(data):
    """Logs performance data to a file."""
    log_file = os.path.join("zero_touch_mikrotik", "data", "performance_log.json")

    if not os.path.exists(log_file):
        with open(log_file, 'w') as f:
            json.dump([], f)

    with open(log_file, 'r+') as f:
        logs = json.load(f)
        logs.append(data)
        f.seek(0)
        json.dump(logs, f, indent=4)

def analyze_feedback(topic, video_duration_sec, youtube_video_id):
    """
    Analyzes feedback, updates the DQN model, and logs performance.
    """
    print("Analyzing feedback and logging performance...")

    # ... (DQN agent and reward calculation remains the same) ...
    agent = DQNAgent()
    feedback = { "ctr": round(random.uniform(0.01, 0.15), 3), "watch_time_avg_sec": random.randint(30, 400) }
    sentiment_score = get_youtube_comments_sentiment(youtube_video_id)
    reward = (feedback["ctr"] * 100) + (feedback["watch_time_avg_sec"] / 10) + (sentiment_score * 20)

    # --- Log Performance ---
    log_data = {
        "timestamp": datetime.now().isoformat(),
        "topic": topic,
        "category": get_topic_category(topic),
        "length": "Short" if video_duration_sec < 300 else "Long",
        "ctr": feedback["ctr"],
        "watch_time_avg_sec": feedback["watch_time_avg_sec"],
        "sentiment_score": sentiment_score,
        "reward": reward
    }
    log_performance_data(log_data)

    # --- Update Model ---
    # ... (The rest of the function remains the same) ...
    category = get_topic_category(topic)
    length = "Short" if video_duration_sec < 300 else "Long"
    state = state_to_tensor(category, length)
    action_idx = ACTION_MAP.get(topic)
    if action_idx is not None:
        action = torch.tensor([[action_idx]], dtype=torch.long)
        reward_tensor = torch.tensor([reward], dtype=torch.float)
        agent.memory.push(state, action, reward_tensor)
        agent.optimize_model()
        agent.save_model()
        print(f"DQN model updated for state ({category}, {length}) and action '{topic}'.")
    else:
        print(f"Warning: Topic '{topic}' not in pre-defined action map. Skipping learning.")

    return feedback
