import os
import json
from datetime import datetime
from instagrapi import Client
from orchestrator import app # Import the Celery app instance

PERFORMANCE_LOG_FILE = os.path.join("zero_touch_mikrotik", "data", "reel_performance.json")

@app.task
def fetch_and_store_analytics(media_pk, topic):
    """Fetches performance metrics for a given Instagram Reel and logs them."""
    print(f"Fetching performance for Reel PK: {media_pk}")

    try:
        cl = Client()
        username = os.environ.get("INSTAGRAM_USERNAME")
        password = os.environ.get("INSTAGRAM_PASSWORD")
        cl.login(username, password)

        # Get media info
        media_info = cl.media_info(media_pk).dict()

        views = media_info.get('play_count', 0)
        likes = media_info.get('like_count', 0)
        comments = media_info.get('comment_count', 0)

        # Engagement rate = (likes + comments) / views
        engagement_rate = ((likes + comments) / views) * 100 if views > 0 else 0

        performance_data = {
            "timestamp": datetime.now().isoformat(),
            "media_pk": media_pk,
            "topic": topic,
            "views": views,
            "likes": likes,
            "comments": comments,
            "engagement_rate": round(engagement_rate, 2)
        }

        print(f"Performance data: {performance_data}")
        log_performance_data(performance_data)

        return performance_data

    except Exception as e:
        print(f"Error fetching Reel performance: {e}")
        return None

def log_performance_data(data):
    """Logs the performance data to a JSON file."""
    if not os.path.exists(PERFORMANCE_LOG_FILE):
        with open(PERFORMANCE_LOG_FILE, 'w') as f:
            json.dump([], f)

    with open(PERFORMANCE_LOG_FILE, 'r+') as f:
        logs = json.load(f)
        # Avoid duplicate entries
        logs = [log for log in logs if log['media_pk'] != data['media_pk']]
        logs.append(data)
        f.seek(0)
        json.dump(logs, f, indent=4)
