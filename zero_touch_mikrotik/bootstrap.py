import os
import subprocess
import sys

def create_project_structure():
    """Creates the necessary directories for the project."""
    print("Creating project structure...")
    directories = [
        "data/scripts",
        "data/audio",
        "data/videos",
        "data/subtitles",
        "data/logs",
        "config"
    ]
    for directory in directories:
        os.makedirs(os.path.join("zero_touch_mikrotik", directory), exist_ok=True)

def create_config_files():
    """Creates the necessary configuration files."""
    print("Creating configuration files...")
    with open("zero_touch_mikrotik/config/scheduler_config.yaml", "w") as f:
        f.write("# Scheduler configuration\n")
    with open("zero_touch_mikrotik/config/hashtags.json", "w") as f:
        f.write("[]")

def install_dependencies():
    """Installs the necessary dependencies using pip."""
    print("Installing dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "celery", "redis", "requests", "beautifulsoup4", "google-api-python-client", "moviepy", "stable-diffusion-sdk", "openai", "coqui-tts", "faster-whisper", "psutil", "Pillow", "pytrends", "tweepy", "pydub", "Flask", "textblob", "textblob-fa", "torch"])

def main():
    """Main function for the bootstrap script."""
    print("Setting up Zero-Touch MikroTik AI Content Factory...")
    create_project_structure()
    create_config_files()
    install_dependencies()
    print("Setup complete!")

if __name__ == "__main__":
    main()
