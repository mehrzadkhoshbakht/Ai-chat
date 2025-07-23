import logging
import os
import yaml

from flask import Flask, render_template, request

from modules.chat_engine import ChatEngine
from modules.text_to_speech import TextToSpeech
from modules.video_generator import VideoGenerator
from modules.scheduler import Scheduler
from modules.uploader import Uploader

# --- Flask App ---
app = Flask(__name__)
scheduler = Scheduler()
uploader = None

# --- Configuration ---
CONFIG_PATH = "config/config.yaml"

def load_config():
    """Loads the YAML configuration file."""
    if not os.path.exists(CONFIG_PATH):
        # Create a default config if it doesn't exist
        default_config = {
            "telegram": {"api_token": "YOUR_TELEGRAM_API_TOKEN", "chat_id": "YOUR_TELEGRAM_CHAT_ID"},
            "elevenlabs": {"api_key": "YOUR_ELEVENLABS_API_KEY"},
            "youtube": {"client_secrets_file": "client_secrets.json"}
        }
        with open(CONFIG_PATH, "w") as f:
            yaml.dump(default_config, f)
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)

# --- Logging ---
def setup_logging():
    """Sets up the logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("app.log"),
            logging.StreamHandler()
        ]
    )

# --- Routes ---
@app.route("/")
def index():
    """Renders the main page."""
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    """Adds a new content generation task to the scheduler."""
    data = request.get_json()
    keywords = data.get("keywords")
    platform = data.get("platform")

    task = {"type": "generate_video", "keywords": keywords, "platform": platform}
    scheduler.add_task(task)

    return {"message": "Task added to the queue."}

@app.route("/api/status")
def status():
    """Returns the system status."""
    return {
        "ai_engine": "online",
        "tts_service": "online",
        "youtube_api": "offline",
        "telegram_bot": "online",
    }

@app.route("/api/tasks")
def tasks():
    """Returns the current task queue."""
    return {"tasks": list(scheduler.task_queue.queue)}

@app.route("/upload", methods=["POST"])
def upload():
    """Uploads a video to a platform."""
    data = request.get_json()
    video_path = data.get("video_path")
    platform = data.get("platform")
    title = data.get("title")
    description = data.get("description")
    caption = data.get("caption")

    if platform == "YouTube":
        result = uploader.upload_to_youtube(video_path, title, description)
    elif platform == "Telegram":
        result = uploader.send_to_telegram(video_path, caption)
    else:
        return {"error": "Unsupported platform."}

    return {"url": result}

# --- Main Application ---
def main():
    """Main function to run the AI-chat application."""
    global uploader
    setup_logging()
    logging.info("Starting AI-chat application...")

    config = load_config()
    uploader = Uploader(config)

    # Initialize modules
    # chat_engine = ChatEngine(config)
    # tts_engine = TextToSpeech(config)
    # video_generator = VideoGenerator(config)

    app.run(host="0.0.0.0", port=8080)

    logging.info("AI-chat application finished.")

if __name__ == "__main__":
    main()