import time
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import os
import telegram

class Uploader:
    def __init__(self, config):
        self.config = config

    def get_youtube_credentials(self):
        """Gets the user's credentials for the YouTube API."""
        client_secrets_file = self.config.get("youtube", {}).get("client_secrets_file", "client_secrets.json")
        scopes = ["https://www.googleapis.com/auth/youtube.upload"]

        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        credentials = flow.run_console()
        return credentials

    def upload_to_youtube(self, video_path, title, description):
        """Uploads a video to YouTube."""
        try:
            credentials = self.get_youtube_credentials()
            youtube = googleapiclient.discovery.build(
                "youtube", "v3", credentials=credentials)

            request = youtube.videos().insert(
                part="snippet,status",
                body={
                    "snippet": {
                        "categoryId": "22",
                        "description": description,
                        "title": title
                    },
                    "status": {
                        "privacyStatus": "private"
                    }
                },
                media_body=googleapiclient.http.MediaFileUpload(video_path)
            )
            response = request.execute()
            return f"https://www.youtube.com/watch?v={response['id']}"
        except Exception as e:
            print(f"Error uploading to YouTube: {e}")
            return None

    def send_to_telegram(self, video_path, caption):
        """Sends a video to Telegram."""
        try:
            bot_token = self.config.get("telegram", {}).get("api_token", "YOUR_TELEGRAM_API_TOKEN")
            chat_id = self.config.get("telegram", {}).get("chat_id", "YOUR_TELEGRAM_CHAT_ID")
            bot = telegram.Bot(token=bot_token)
            with open(video_path, 'rb') as video:
                message = bot.send_video(chat_id=chat_id, video=video, caption=caption)
            return f"https://t.me/{message.chat.username}/{message.message_id}"
        except Exception as e:
            print(f"Error sending to Telegram: {e}")
            return None
