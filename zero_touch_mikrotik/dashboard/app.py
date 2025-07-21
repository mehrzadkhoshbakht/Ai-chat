from flask import Flask, render_template, send_from_directory, redirect, url_for, flash, jsonify, request
from celery import Celery
import os
import glob
import json

app = Flask(__name__)
app.secret_key = os.urandom(24) # Needed for flashing messages
celery_app = Celery('orchestrator', broker='redis://redis:6379/0', backend='redis://redis:6379/0')

LOG_DIR = '/app/data/logs' # Kept for raw logs if needed
BACKUP_DIR = '/app/data/backup'
PERFORMANCE_LOG = '/app/data/performance_log.json'
ACTIVITY_LOG = '/app/data/activity.log'
REEL_PERFORMANCE_LOG = '/app/data/reel_performance.json'

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

def get_activity_logs():
    """Reads the structured activity log."""
    if not os.path.exists(ACTIVITY_LOG):
        return []

    with open(ACTIVITY_LOG, 'r') as f:
        # Read last 50 lines to keep the dashboard snappy
        lines = f.readlines()[-50:]

    logs = [json.loads(line) for line in lines]
    return sorted(logs, key=lambda x: x['timestamp'], reverse=True)

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
    activity_logs = get_activity_logs()
    videos = get_videos()
    return render_template('index.html', status=status, activity_logs=activity_logs, videos=videos)

@app.route('/trigger', methods=['POST'])
def trigger_task():
    """Manually triggers the content creation pipeline."""
    try:
        # The task name must match how Celery sees it: <module>.<task_name>
        celery_app.send_task('orchestrator.main_task')
        flash('Content creation pipeline has been triggered successfully!', 'success')
    except Exception as e:
        flash(f'Error triggering task: {e}', 'error')
    return redirect(url_for('index'))

@app.route('/videos/<path:filename>')
def download_video(filename):
    return send_from_directory(BACKUP_DIR, filename, as_attachment=True)

@app.route('/api/performance_data')
def performance_data():
    """API endpoint to serve AI model performance data."""
    if not os.path.exists(PERFORMANCE_LOG):
        return jsonify([])
    with open(PERFORMANCE_LOG, 'r') as f:
        data = json.load(f)
    return jsonify(data[-30:])

@app.route('/api/reel_performance')
def reel_performance_data():
    """API endpoint to serve Reel performance data."""
    if not os.path.exists(REEL_PERFORMANCE_LOG):
        return jsonify([])
    with open(REEL_PERFORMANCE_LOG, 'r') as f:
        data = json.load(f)
    return jsonify(data[-30:])

@app.route('/api/publish', methods=['POST'])
def api_publish():
    """API endpoint to trigger content creation externally."""
    auth_header = request.headers.get('Authorization')
    api_token = os.environ.get('API_ACCESS_TOKEN')

    if not api_token:
        return jsonify({"status": "error", "message": "API is not configured on the server."}), 500

    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"status": "error", "message": "Authorization header is missing or invalid."}), 401

    token = auth_header.split(' ')[1]
    if token != api_token:
        return jsonify({"status": "error", "message": "Invalid API token."}), 403

    # --- Input Validation ---
    if not request.is_json:
        return jsonify({"status": "error", "message": "Request must be JSON."}), 400

    data = request.get_json()
    topic = data.get('topic')

    if not topic:
        return jsonify({"status": "error", "message": "Missing 'topic' in request body."}), 400

    # --- Trigger Celery Task ---
    try:
        length_category = data.get('length_category', 'Short') # Default to 'Short' if not provided
        celery_app.send_task(
            'orchestrator.main_task',
            kwargs={'topic': topic, 'length_category': length_category}
        )
        return jsonify({"status": "success", "message": f"Content creation for topic '{topic}' has been queued."})
    except Exception as e:
        return jsonify({"status": "error", "message": f"Failed to queue task: {e}"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=False)
