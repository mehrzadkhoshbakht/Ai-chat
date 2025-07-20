import os
import shutil

def manage_storage(topic):
    """
    Manages storage by backing up finished media and cleaning up local files.
    """
    print("Managing storage...")

    # --- Backup Placeholder ---
    # In a real implementation, you would use a library like `boto3` to upload to S3
    # or another object storage service.

    backup_dir = os.path.join("zero_touch_mikrotik", "data", "backup", topic.replace(' ', '_'))
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    print(f"Backing up files to {backup_dir}...")

    # Move final video to backup
    video_path = os.path.join("zero_touch_mikrotik", "data", "videos", f"{topic.replace(' ', '_')}.mp4")
    if os.path.exists(video_path):
        shutil.move(video_path, os.path.join(backup_dir, os.path.basename(video_path)))
        print(f"Backed up video: {video_path}")

    # --- Cleanup ---
    print("Cleaning up local temporary files...")

    # Clean up script, audio, and images for the topic
    data_dirs = ["scripts", "audio", "images", "subtitles"]
    for data_dir in data_dirs:
        dir_path = os.path.join("zero_touch_mikrotik", "data", data_dir)
        if not os.path.exists(dir_path):
            continue
        for f in os.listdir(dir_path):
            if f.startswith(topic.replace(' ', '_')):
                file_path = os.path.join(dir_path, f)
                os.remove(file_path)
                print(f"Removed {file_path}")

    print("Storage management complete.")
    return True
