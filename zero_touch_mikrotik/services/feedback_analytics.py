import os
import random
import torch
from services.ai_model import DQNAgent, state_to_tensor, get_topic_category, ACTION_MAP

def get_youtube_comments_sentiment(video_id):
    # This function would remain the same, fetching comments and analyzing them
    # For brevity, we assume it's implemented elsewhere or remains as a placeholder
    print(f"Fetching sentiment for video {video_id} (placeholder)...")
    return random.uniform(-0.5, 0.5)

def analyze_feedback(topic, video_duration_sec, youtube_video_id):
    """
    Analyzes feedback and updates the centralized DQN model.
    """
    print("Analyzing feedback with centralized DQN model...")

    # --- Initialize Agent ---
    agent = DQNAgent()

    # --- Get Feedback and Calculate Reward ---
    # Placeholder for real analytics
    feedback = { "ctr": round(random.uniform(0.01, 0.15), 3), "watch_time_avg_sec": random.randint(30, 400) }
    sentiment_score = get_youtube_comments_sentiment(youtube_video_id)
    reward = (feedback["ctr"] * 100) + (feedback["watch_time_avg_sec"] / 10) + (sentiment_score * 20)

    # --- Prepare Tensors for Memory ---
    category = get_topic_category(topic)
    length = "Short" if video_duration_sec < 300 else "Long"
    state = state_to_tensor(category, length)

    action_idx = ACTION_MAP.get(topic)
    if action_idx is None:
        print(f"Warning: Topic '{topic}' not in pre-defined action map. Skipping learning.")
        return feedback

    action = torch.tensor([[action_idx]], dtype=torch.long)
    reward_tensor = torch.tensor([reward], dtype=torch.float)

    # --- Store experience and optimize ---
    agent.memory.push(state, action, reward_tensor)
    agent.optimize_model()
    agent.save_model()

    print(f"DQN model updated for state ({category}, {length}) and action '{topic}'.")
    return feedback
