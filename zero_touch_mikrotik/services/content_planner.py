import random

def plan_content(trending_topics):
    """
    Selects a topic from the list of trending topics.
    """
    print("Planning content...")
    if not trending_topics:
        print("No trending topics found. Using a default topic.")
        return "Default Topic: MikroTik Router Configuration"

    selected_topic = random.choice(trending_topics)
    print(f"Selected topic: {selected_topic}")
    return selected_topic
