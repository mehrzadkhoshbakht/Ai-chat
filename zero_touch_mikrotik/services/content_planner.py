import random
import os
import pickle

# We need access to the Q-learning model to make informed decisions
class QLearningModel:
    def __init__(self, model_path='q_table.pkl'):
        self.model_path = os.path.join("zero_touch_mikrotik", "data", model_path)
        self.q_table = self.load_model()

    def load_model(self):
        if os.path.exists(self.model_path):
            with open(self.model_path, 'rb') as f:
                return pickle.load(f)
        return {}

    def get_q_value(self, state, action):
        return self.q_table.get((state, action), 0.0)

    def choose_best_topic(self, topics):
        if not topics:
            return None

        state = "topics"

        # Filter out topics that have never been tried before
        known_topics = [t for t in topics if self.get_q_value(state, t) > 0]

        if not known_topics:
            # If no topics have a Q-value, or all are 0, pick a random one to explore
            return random.choice(topics)

        # Choose the topic with the highest Q-value among the known ones
        q_values = [self.get_q_value(state, t) for t in known_topics]
        max_q = max(q_values)
        best_topics = [known_topics[i] for i, q in enumerate(q_values) if q == max_q]

        return random.choice(best_topics)

def plan_content(trending_topics):
    """
    Selects a topic from the list of trending topics using the Q-learning model.
    """
    print("Planning content using Q-learning model...")

    if not trending_topics:
        print("No trending topics found. Using a default topic.")
        return "Default Topic: MikroTik Router Configuration"

    # Use the Q-learning model to choose the best topic
    model = QLearningModel()

    # Add some randomness to explore new topics occasionally
    if random.uniform(0, 1) < 0.2: # 20% chance to explore a random topic
        print("Exploring a random topic...")
        selected_topic = random.choice(trending_topics)
    else:
        print("Choosing best topic based on past performance...")
        selected_topic = model.choose_best_topic(trending_topics)
        if selected_topic is None:
             selected_topic = random.choice(trending_topics)

    print(f"Selected topic: {selected_topic}")
    return selected_topic
