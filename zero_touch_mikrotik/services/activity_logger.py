import os
import json
from datetime import datetime

LOG_FILE = os.path.join("zero_touch_mikrotik", "data", "activity.log")

def log_activity(platform, topic, success, details=""):
    """Logs a publishing activity to a structured log file."""

    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "platform": platform,
        "topic": topic,
        "status": "Success" if success else "Failure",
        "details": str(details)
    }

    # Ensure the log file exists
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'w') as f:
            f.write("") # Create the file

    with open(LOG_FILE, 'a') as f:
        f.write(json.dumps(log_entry) + "\n")
