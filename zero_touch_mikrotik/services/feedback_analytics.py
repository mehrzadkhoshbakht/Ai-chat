import json
import os
import random
import pickle

class QLearningModel:
    def __init__(self, model_path='q_table.pkl', learning_rate=0.1, discount_factor=0.9, exploration_rate=0.1):
        self.model_path = os.path.join("zero_touch_mikrotik", "data", model_path)
        self.lr = learning_rate
        self.gamma = discount_factor
        self.epsilon = exploration_rate
        self.q_table = self.load_model()

    def load_model(self):
        if os.path.exists(self.model_path):
            with open(self.model_path, 'rb') as f:
                return pickle.load(f)
        return {}

    def save_model(self):
        with open(self.model_path, 'wb') as f:
            pickle.dump(self.q_table, f)

    def get_q_value(self, state, action):
        return self.q_table.get((state, action), 0.0)

    def choose_action(self, state, actions):
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(actions) # Explore

        q_values = [self.get_q_value(state, a) for a in actions]
        max_q = max(q_values)

        # If multiple actions have the same max Q-value, choose one randomly
        best_actions = [actions[i] for i, q in enumerate(q_values) if q == max_q]
        return random.choice(best_actions)

    def update_q_value(self, state, action, reward, next_state_best_q):
        old_value = self.get_q_value(state, action)
        new_value = old_value + self.lr * (reward + self.gamma * next_state_best_q - old_value)
        self.q_table[(state, action)] = new_value

def analyze_feedback(topic):
    """
    Analyzes feedback and updates the Q-learning model.
    """
    print("Analyzing feedback...")

    # --- Placeholder for fetching real analytics ---
    feedback = {
        "topic": topic,
        "ctr": round(random.uniform(0.01, 0.15), 3),
        "watch_time_avg_sec": random.randint(30, 400),
    }
    print(f"Feedback for '{topic}': {feedback}")

    # --- Update Q-learning Model ---
    model = QLearningModel()

    # Define state, action, and reward
    state = "topics" # A general state for all topics
    action = topic

    # Simple reward function
    reward = (feedback["ctr"] * 100) + (feedback["watch_time_avg_sec"] / 10)

    # In a more complex model, next_state would be different. Here, we assume it's the same.
    # We don't have a future state, so the next_state_best_q is 0.
    model.update_q_value(state, action, reward, 0)

    model.save_model()
    print("Q-learning model updated and saved.")

    return feedback
