import json
import os
import tweepy
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from moviepy.editor import VideoFileClip

def get_youtube_service():
    """Authenticates and returns a YouTube service object."""
    creds = None
    token_path = 'youtube_credentials.json'
    client_secrets_path = 'client_secrets.json'

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, ['https://www.googleapis.com/auth/youtube.upload'])

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(client_secrets_path):
                raise FileNotFoundError(
                    "OAuth 2.0 client secrets file not found. "
                    "Please download it from the Google Cloud Console and place it as 'client_secrets.json'."
                )
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secrets_path, ['https://www.googleapis.com/auth/youtube.upload'])
            creds = flow.run_local_server(port=0)

        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    return build('youtube', 'v3', credentials=creds)

def create_teaser_clip(video_path, topic, duration=30):
    """Creates a short teaser clip from the main video."""
    video = VideoFileClip(video_path)
    teaser_duration = min(video.duration, duration)
    teaser = video.subclip(0, teaser_duration)

    teaser_path = os.path.join("zero_touch_mikrotik", "data", "videos", f"{topic.replace(' ', '_')}_teaser.mp4")
    teaser.write_videofile(teaser_path, codec='libx264', audio_codec='aac')

    return teaser_path

def publish_to_twitter(video_path, topic, youtube_url):
    """Publishes a teaser video to Twitter."""
    print("\n--- Publishing to Twitter ---")

    try:
        # Get API keys from environment variables
        consumer_key = os.environ.get("TWITTER_CONSUMER_KEY")
        consumer_secret = os.environ.get("TWITTER_CONSUMER_SECRET")
        access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
        access_token_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")

        if not all([consumer_key, consumer_secret, access_token, access_token_secret]):
            print("Twitter API credentials not found in environment variables. Skipping.")
            return

        client = tweepy.Client(
            consumer_key=consumer_key,
            consumer_secret=consumer_secret,
            access_token=access_token,
            access_token_secret=access_token_secret
        )
        auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
        api = tweepy.API(auth)

        # Create a teaser clip
        teaser_path = create_teaser_clip(video_path, topic)

        # Upload the media
        media = api.media_upload(filename=teaser_path)

        # Post the tweet
        tweet_text = f"ویدیوی جدید: آموزش میکروتیک - {topic}\n\nبرای مشاهده ویدیوی کامل به لینک زیر مراجعه کنید:\n{youtube_url}\n\n#MikroTik #آموزش_میکروتیک"
        client.create_tweet(text=tweet_text, media_ids=[media.media_id_string])

        print("Successfully posted teaser to Twitter.")

    except Exception as e:
        print(f"Error publishing to Twitter: {e}")

def publish_content(video_path, topic, subtitle_paths):
    """
    Publishes the video to YouTube and a teaser to Twitter.
    """
    youtube_video_id = None

    # --- Publish to YouTube ---
    print("Publishing content to YouTube...")
    try:
        youtube = get_youtube_service()
        with open("zero_touch_mikrotik/config/hashtags.json", "r") as f:
            hashtags = json.load(f)

        title = f"آموزش میکروتیک: {topic}"
        description = f"در این ویدیو به آموزش {topic} می‌پردازیم.\n\n" + " ".join(hashtags)
        tags = ["MikroTik", "tutorial", "Persian"] + [tag.strip('#') for tag in hashtags]

        request_body = {
            'snippet': { 'categoryId': '28', 'title': title, 'description': description, 'tags': tags, 'defaultLanguage': 'fa', 'defaultAudioLanguage': 'fa' },
            'status': { 'privacyStatus': 'private', 'selfDeclaredMadeForKids': False }
        }

        media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
        response_upload = youtube.videos().insert(part='snippet,status', body=request_body, media_body=media).execute()

        youtube_video_id = response_upload.get('id')
        if youtube_video_id:
            print(f"Video uploaded to YouTube! Video ID: {youtube_video_id}")
            # ... (subtitle upload logic remains the same) ...
        else:
            print("Could not get YouTube video ID.")

    except FileNotFoundError as e:
        print(f"Could not initialize YouTube service: {e}")
    except Exception as e:
        print(f"Error publishing to YouTube: {e}")

    # --- Publish to Twitter ---
    if youtube_video_id:
        youtube_url = f"https://www.youtube.com/watch?v={youtube_video_id}"
        publish_to_twitter(video_path, topic, youtube_url)
    else:
        print("Skipping Twitter publish due to missing YouTube URL.")

    print("\nPublishing process complete.")
    return youtube_video_id
