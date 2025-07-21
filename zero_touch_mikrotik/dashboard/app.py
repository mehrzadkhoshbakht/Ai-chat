from flask import Flask, render_template, send_from_directory
from celery import Celery
import os
import glob

app = Flask(__name__)
celery_app = Celery('zero_touch_mikrotik', broker='redis://redis:6379/0')

LOG_DIR = '/app/data/logs'
BACKUP_DIR = '/app/data/backup'

def get_celery_status():
    try:
        stats = celery_app.control.inspect().stats()
        if not stats:
            return "Celery worker not available."

        worker_name = list(stats.keys())[0]
        active_tasks = celery_app.control.inspect().active()

        if active_tasks and active_tasks[worker_name]:
            return f"Busy ({len(active_tasks[worker_name])} task(s) running)"
        return "Idle"
    except Exception as e:
        return f"Error connecting to Celery: {e}"

def get_logs():
    if not os.path.exists(LOG_DIR):
        return ["Log directory not found."]

    log_files = glob.glob(os.path.join(LOG_DIR, '*.log'))
    if not log_files:
        return ["No log files found."]

    # Get the latest log file
    latest_log_file = max(log_files, key=os.path.getctime)

    with open(latest_log_file, 'r', encoding='utf-8') as f:
        # Read the last 100 lines
        lines = f.readlines()[-100:]
        return [line.strip() for line in lines]

def get_videos():
    if not os.path.exists(BACKUP_DIR):
        return []

    videos = []
    for video_dir in os.listdir(BACKUP_DIR):
        full_dir_path = os.path.join(BACKUP_DIR, video_dir)
        if os.path.isdir(full_dir_path):
            for file in os.listdir(full_dir_path):
                if file.endswith(".mp4"):
                    videos.append(os.path.join(video_dir, file))
    return sorted(videos, reverse=True)


@app.route('/')
def index():
    status = get_celery_status()
    logs = get_logs()
    videos = get_videos()
    return render_template('index.html', status=status, logs=logs, videos=videos)

@app.route('/videos/<path:filename>')
def download_video(filename):
    return send_from_directory(BACKUP_DIR, filename, as_attachment=True)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)
