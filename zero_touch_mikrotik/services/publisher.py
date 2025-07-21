import os
import tweepy
from moviepy.editor import VideoFileClip
from instagrapi import Client
from googleapiclient.http import MediaFileUpload
from services.notifier import send_success_notification
from services.activity_logger import log_activity
from services.analytics import fetch_and_store_analytics
from orchestrator import app # Import the Celery app instance

# --- Helper functions (get_youtube_service, create_reel_clip) remain the same ---
# For brevity, their code is assumed to be here.

@app.task
def publish_to_youtube(video_path, topic, subtitle_paths):
    """Celery task to publish a video to YouTube."""
    print(f"Executing YouTube publish task for: {topic}")
    try:
        from services.publisher import get_youtube_service # Local import to avoid circular dependency issues
        youtube = get_youtube_service()
        # ... (Full YouTube upload logic) ...
        youtube_video_id = "placeholder_youtube_id" # From API response
        log_activity("YouTube", topic, True, f"Video ID: {youtube_video_id}")
        print(f"Successfully published to YouTube. Video ID: {youtube_video_id}")
        return youtube_video_id
    except Exception as e:
        log_activity("YouTube", topic, False, str(e))
        print(f"Error in YouTube publish task: {e}")
        return None

@app.task
def publish_to_twitter(video_path, topic, youtube_url):
    """Celery task to publish a teaser to Twitter."""
    print(f"Executing Twitter publish task for: {topic}")
    try:
        # ... (Full Twitter publishing logic) ...
        log_activity("Twitter", topic, True)
        print("Successfully posted teaser to Twitter.")
    except Exception as e:
        log_activity("Twitter", topic, False, str(e))
        print(f"Error in Twitter publish task: {e}")

@app.task
def publish_to_instagram(video_path, topic):
    """Celery task to publish a Reel to Instagram and schedule analytics."""
    print(f"Executing Instagram publish task for: {topic}")
    try:
        from services.publisher import create_reel_clip # Local import
        cl = Client()
        cl.login(os.environ.get("INSTAGRAM_USERNAME"), os.environ.get("INSTAGRAM_PASSWORD"))
        reel_path = create_reel_clip(video_path, topic)
        caption = f"آموزش میکروتیک: {topic}\n\n#MikroTik #tutorial"

        media = cl.video_upload(path=reel_path, caption=caption)
        media_pk = media.pk

        log_activity("Instagram", topic, True, f"Media PK: {media_pk}")
        send_success_notification(topic, "Instagram")
        print(f"Successfully posted Reel to Instagram. PK: {media_pk}")

        # Schedule the analytics task to run in 24 hours
        fetch_and_store_analytics.apply_async(args=[media_pk, topic], countdown=86400)
        print(f"Scheduled analytics task for Reel PK {media_pk} in 24 hours.")

    except Exception as e:
        log_activity("Instagram", topic, False, str(e))
        print(f"Error in Instagram publish task: {e}")

# --- Helper functions that need to be accessible but not tasks ---
def get_youtube_service():
    # ... (Implementation remains the same) ...
    pass

def create_reel_clip(video_path, topic, duration=90):
    # ... (Implementation remains the same) ...
    video = VideoFileClip(video_path)
    reel_duration = min(video.duration, duration)
    reel = video.subclip(0, reel_duration)

    reel_path = os.path.join("zero_touch_mikrotik", "data", "videos", f"{topic.replace(' ', '_')}_reel.mp4")
    reel.write_videofile(reel_path, codec='libx264', audio_codec='aac')

    return reel_path
