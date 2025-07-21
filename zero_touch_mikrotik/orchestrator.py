import traceback
from celery import Celery
from celery.schedules import crontab
from services.resource_watcher import is_system_idle
from services.trend_scanner import get_trending_topics
from services.content_planner import plan_content
from services.script_generator import generate_script
from services.voice_generator import generate_voice
from services.visual_generator import generate_visuals
from services.video_assembler import assemble_video
from services.subtitle_translator import generate_subtitles
from services.publisher import publish_content
from services.feedback_analytics import analyze_feedback
from services.storage_manager import manage_storage
from services.notifier import send_error_notification

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
def main_task():
    """
    The main task that orchestrates the entire content creation process.
    """
    print("Checking system resources...")
    if not is_system_idle():
        print("System is not idle. Postponing content creation.")
        return

    print("Starting content creation pipeline...")

    try:
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

        # 6. Assemble video
        video_path, video_duration_sec = assemble_video(visual_paths, audio_path, topic)

        # 7. Generate subtitles and translations
        subtitle_paths = generate_subtitles(audio_path, topic)

        # 8. Publish video
        youtube_video_id = publish_content(video_path, topic, subtitle_paths)

        # 9. Analyze feedback
        analyze_feedback(topic, video_duration_sec, youtube_video_id)

        # 10. Manage storage
        manage_storage(topic)

        print("Content creation pipeline finished successfully.")

    except Exception as e:
        error_message = f"An error occurred in the pipeline: {e}"
        traceback_info = traceback.format_exc()
        print(error_message)
        print(traceback_info)
        send_error_notification(error_message, traceback_info)

if __name__ == '__main__':
    # For direct execution without Celery worker (for testing)
    main_task()
