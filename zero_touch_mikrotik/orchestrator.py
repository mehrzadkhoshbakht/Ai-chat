from celery import Celery
from services.resource_watcher import is_system_idle

app = Celery('zero_touch_mikrotik', broker='redis://localhost:6379/0')

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
    # 2. Scan for trending topics
    # 3. Plan content
    # 4. Generate script
    # 5. Generate voice
    # 6. Generate visuals
    # 7. Assemble video
    # 8. Generate subtitles and translations
    # 9. Publish video
    # 10. Analyze feedback
    # 11. Manage storage
    print("Content creation pipeline finished.")

if __name__ == '__main__':
    main_task.delay()
