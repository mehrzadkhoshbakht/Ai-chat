import time

class Uploader:
    def __init__(self, config):
        self.config = config

    def upload_to_youtube(self, video_path, title, description):
        """Mocks uploading a video to YouTube."""
        print(f"Uploading video to YouTube: {video_path}")
        print(f"Title: {title}")
        print(f"Description: {description}")
        # Simulate a delay for uploading the video
        time.sleep(10)
        print("Video uploaded to YouTube successfully.")
        return f"https://www.youtube.com/watch?v=mock_video_id"

    def send_to_telegram(self, video_path, caption):
        """Mocks sending a video to Telegram."""
        print(f"Sending video to Telegram: {video_path}")
        print(f"Caption: {caption}")
        # Simulate a delay for sending the video
        time.sleep(5)
        print("Video sent to Telegram successfully.")
        return "https://t.me/mock_channel/mock_message_id"
