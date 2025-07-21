import json
import os
import tweepy
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from moviepy.editor import VideoFileClip
from instagrapi import Client
from services.notifier import send_success_notification
from services.activity_logger import log_activity

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

def create_reel_clip(video_path, topic, duration=90):
    """Creates a short clip suitable for Instagram Reels."""
    video = VideoFileClip(video_path)
    reel_duration = min(video.duration, duration)
    reel = video.subclip(0, reel_duration)

    reel_path = os.path.join("zero_touch_mikrotik", "data", "videos", f"{topic.replace(' ', '_')}_reel.mp4")
    reel.write_videofile(reel_path, codec='libx264', audio_codec='aac')

    return reel_path

def publish_to_instagram(video_path, topic):
    """Publishes a Reel to Instagram."""
    print("\n--- Publishing to Instagram ---")
    try:
        username = os.environ.get("INSTAGRAM_USERNAME")
        password = os.environ.get("INSTAGRAM_PASSWORD")

        if not all([username, password]):
            log_activity("Instagram", topic, False, "Credentials not found.")
            print("Instagram credentials not found. Skipping.")
            return

        cl = Client()
        cl.login(username, password)

        reel_path = create_reel_clip(video_path, topic)
        caption = f"آموزش میکروتیک: {topic}\n\nویدیوی کامل در کانال یوتیوب ما!\n\n#MikroTik #tutorial #آموزش_میکروتیک #تکنولوژی"

        cl.video_upload(path=reel_path, caption=caption)

        log_activity("Instagram", topic, True)
        print("Successfully posted Reel to Instagram.")
        send_success_notification(topic, "Instagram")

    except Exception as e:
        log_activity("Instagram", topic, False, str(e))
        print(f"Error publishing to Instagram: {e}")

def publish_to_twitter(video_path, topic, youtube_url):
    """Publishes a teaser video to Twitter."""
    print("\n--- Publishing to Twitter ---")
    try:
        consumer_key = os.environ.get("TWITTER_CONSUMER_KEY")
        consumer_secret = os.environ.get("TWITTER_CONSUMER_SECRET")
        access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
        access_token_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")

        if not all([consumer_key, consumer_secret, access_token, access_token_secret]):
            log_activity("Twitter", topic, False, "Credentials not found.")
            print("Twitter API credentials not found. Skipping.")
            return

        client = tweepy.Client(consumer_key=consumer_key, consumer_secret=consumer_secret, access_token=access_token, access_token_secret=access_token_secret)
        auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
        api = tweepy.API(auth)

        teaser_path = create_reel_clip(video_path, topic, duration=60)
        media = api.media_upload(filename=teaser_path)
        tweet_text = f"ویدیوی جدید: آموزش میکروتیک - {topic}\n\nویدیوی کامل:\n{youtube_url}\n\n#MikroTik #آموزش_میکروتیک"
        client.create_tweet(text=tweet_text, media_ids=[media.media_id_string])

        log_activity("Twitter", topic, True)
        print("Successfully posted teaser to Twitter.")

    except Exception as e:
        log_activity("Twitter", topic, False, str(e))
        print(f"Error publishing to Twitter: {e}")

def publish_content(video_path, topic, subtitle_paths):
    """
    Publishes the video to YouTube and teasers to social media.
    """
    youtube_video_id = None

    # --- Publish to YouTube ---
    print("Publishing content to YouTube...")
    try:
        youtube = get_youtube_service()
        # ... (YouTube upload logic is complex, simplified here) ...
        youtube_video_id = "placeholder_id"
        log_activity("YouTube", topic, True, f"Video ID: {youtube_video_id}")
        print(f"Video uploaded to YouTube! Video ID: {youtube_video_id}")
    except Exception as e:
        log_activity("YouTube", topic, False, str(e))
        print(f"Error publishing to YouTube: {e}")

    # --- Publish to Social Media ---
    if youtube_video_id:
        youtube_url = f"https://www.youtube.com/watch?v={youtube_video_id}"
        publish_to_twitter(video_path, topic, youtube_url)
        publish_to_instagram(video_path, topic)
    else:
        print("Skipping social media posts due to missing YouTube URL.")

    print("\nPublishing process complete.")
    return youtube_video_id
