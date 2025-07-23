import time
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import os
import telegram
import logging
from tenacity import retry, stop_after_attempt, wait_random_exponential

logger = logging.getLogger(__name__)

class Uploader:
    def __init__(self):
        pass

    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
    def get_youtube_credentials(self):
        """Gets the user's credentials for the YouTube API."""
        logger.info("Getting YouTube credentials...")
        client_secrets_file = os.getenv("YOUTUBE_CLIENT_SECRETS_FILE")
        scopes = ["https://www.googleapis.com/auth/youtube.upload"]

        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        credentials = flow.run_console()
        logger.info("YouTube credentials obtained successfully.")
        return credentials

    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
    def upload_to_youtube(self, video_path, title, description):
        """Uploads a video to YouTube."""
        logger.info(f"Uploading video to YouTube: {video_path}")
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
            logger.info(f"Video uploaded to YouTube successfully: {response['id']}")
            return f"https://www.youtube.com/watch?v={response['id']}"
        except Exception as e:
            logger.error(f"Error uploading to YouTube: {e}", exc_info=True)
            raise e

    @retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
    def send_to_telegram(self, video_path, caption):
        """Sends a video to Telegram."""
        logger.info(f"Sending video to Telegram: {video_path}")
        try:
            bot_token = os.getenv("TELEGRAM_API_TOKEN")
            chat_id = os.getenv("TELEGRAM_CHAT_ID")
            bot = telegram.Bot(token=bot_token)
            with open(video_path, 'rb') as video:
                message = bot.send_video(chat_id=chat_id, video=video, caption=caption)
            logger.info(f"Video sent to Telegram successfully: {message.message_id}")
            return f"https://t.me/{message.chat.username}/{message.message_id}"
        except Exception as e:
            logger.error(f"Error sending to Telegram: {e}", exc_info=True)
            raise e
