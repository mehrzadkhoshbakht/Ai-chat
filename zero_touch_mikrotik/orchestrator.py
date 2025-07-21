import traceback
from celery import Celery
from celery.schedules import crontab
from services.decrypt_secrets import load_decrypted_env

# Load decrypted environment variables at the very beginning
load_decrypted_env()

from services.resource_watcher import is_system_idle
from services.trend_scanner import get_trending_topics
from services.content_planner import plan_content
from services.script_generator import generate_script
from services.voice_generator import generate_voice
from services.visual_generator import generate_visuals
from services.video_assembler import assemble_video
from services.subtitle_translator import generate_subtitles
from services import publisher
from services.feedback_analytics import analyze_feedback
from services.storage_manager import manage_storage
from services.notifier import send_error_notification
from datetime import datetime, timedelta

app = Celery('zero_touch_mikrotik', broker='redis://redis:6379/0')

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Add the main task to the schedule to run every 24 hours
    sender.add_periodic_task(
        crontab(hour=0, minute=0), # Executes daily at midnight
        main_task.s(),
        name='create content every 24 hours'
    )

@app.task
def main_task(topic=None, length_category=None):
    """
    The main task that orchestrates the content creation process.
    Can be run with specific parameters or automatically.
    """
    print("Checking system resources...")
    if not is_system_idle():
        print("System is not idle. Postponing content creation.")
        return

    print("Starting content creation pipeline...")

    try:
        if topic:
            print(f"Manual run for topic: {topic}")
            estimated_duration = 180 if length_category == "Short" else 600
        else:
            # 1. Scan for trending topics
            trending_topics = get_trending_topics()
            # 2. Plan content
            topic, estimated_duration = plan_content(trending_topics)

        # 3. Generate script
        script_path = generate_script(topic, estimated_duration)

        # 4. Generate voice
        audio_path = generate_voice(script_path)

        # 5. Generate visuals
        visual_paths = generate_visuals(topic)

        # 6. Generate subtitles and translations (SRT path is needed for assembly)
        subtitle_paths = generate_subtitles(audio_path, topic)
        srt_path_fa = next((s for s in subtitle_paths if s.endswith("_fa.srt")), None)
        if not srt_path_fa:
            raise ValueError("Farsi SRT file not found, cannot proceed with video assembly.")

        # 7. Assemble video with burned-in subtitles
        video_path, video_duration_sec = assemble_video(visual_paths, audio_path, srt_path_fa, topic)

        # 8. Schedule all publications and subsequent tasks
        schedule_publications.delay(video_path, topic, subtitle_paths, video_duration_sec)

        print("Content creation and publication scheduling complete.")

    except Exception as e:
        error_message = f"An error occurred in the pipeline: {e}"
        traceback_info = traceback.format_exc()
        print(error_message)
        print(traceback_info)
        send_error_notification(error_message, traceback_info)

@app.task
def schedule_publications(video_path, topic, subtitle_paths, video_duration_sec):
    """
    Schedules the publishing tasks and subsequent analysis and cleanup.
    """
    # 1. Publish to YouTube immediately.
    # We use a chain to ensure subsequent tasks only run if YouTube upload is successful.
    youtube_task = publisher.publish_to_youtube.s(video_path, topic, subtitle_paths)

    # Schedule subsequent tasks in a chain
    # Note: The result of the YouTube task (video_id) is passed to the next task in the chain.
    chain = youtube_task | app.signature(
        'orchestrator.post_youtube_actions',
        args=(video_path, topic, video_duration_sec)
    )
    chain.apply_async()

@app.task
def post_youtube_actions(youtube_video_id, video_path, topic, video_duration_sec):
    """
    Tasks to run after YouTube publication: social media, analysis, and cleanup.
    """
    if not youtube_video_id:
        print("YouTube publication failed. Skipping subsequent tasks.")
        return

    youtube_url = f"https://www.youtube.com/watch?v={youtube_video_id}"

    # 2. Schedule Instagram Reel for 6 PM
    now = datetime.utcnow()
    six_pm_today = now.replace(hour=18, minute=0, second=0, microsecond=0)
    if now > six_pm_today:
        six_pm_today += timedelta(days=1) # If it's already past 6 PM, schedule for tomorrow
    publisher.publish_to_instagram.s(video_path, topic).apply_async(eta=six_pm_today)

    # 3. Schedule Twitter post for 10 AM tomorrow
    ten_am_tomorrow = (now + timedelta(days=1)).replace(hour=10, minute=0, second=0, microsecond=0)
    publisher.publish_to_twitter.s(video_path, topic, youtube_url).apply_async(eta=ten_am_tomorrow)

    # 4. Analyze feedback
    analyze_feedback(topic, video_duration_sec, youtube_video_id)

    # 5. Manage storage
    manage_storage(topic)
    print("All post-YouTube actions have been scheduled or executed.")

if __name__ == '__main__':
    # For direct execution without Celery worker (for testing)
    main_task()
