import logging
import os
import yaml

from modules.chat_engine import ChatEngine
from modules.text_to_speech import TextToSpeech
from modules.video_generator import VideoGenerator

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

# --- Main Application ---
def main():
    """Main function to run the AI-chat application."""
    setup_logging()
    logging.info("Starting AI-chat application...")

    config = load_config()

    # Initialize modules
    # chat_engine = ChatEngine(config)
    # tts_engine = TextToSpeech(config)
    # video_generator = VideoGenerator(config)

    logging.info("AI-chat application finished.")

if __name__ == "__main__":
    main()