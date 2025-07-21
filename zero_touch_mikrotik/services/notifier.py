import os
import yagmail
from datetime import datetime

def send_error_notification(error_message, traceback_info):
    """Sends an email notification when a critical error occurs."""

    email_user = os.environ.get("EMAIL_USER")
    email_password = os.environ.get("EMAIL_PASSWORD")
    email_to = os.environ.get("EMAIL_TO")

    if not all([email_user, email_password, email_to]):
        print("Email credentials not found. Cannot send notification.")
        return

    try:
        yag = yagmail.SMTP(email_user, email_password)
        subject = f"🚨 Critical Error in Zero-Touch MikroTik Factory"
        body = f"""Hello,\n\nA critical error occurred at {datetime.now().isoformat()}.\n\nError:\n{error_message}\n\nTraceback:\n<pre>{traceback_info}</pre>\n\n- The Autonomous System"""
        yag.send(to=email_to, subject=subject, contents=body)
        print("Successfully sent error notification email.")
    except Exception as e:
        print(f"Failed to send error notification email: {e}")

def send_success_notification(topic, platform):
    """Sends an email notification upon successful publication."""

    email_user = os.environ.get("EMAIL_USER")
    email_password = os.environ.get("EMAIL_PASSWORD")
    email_to = os.environ.get("EMAIL_TO")

    if not all([email_user, email_password, email_to]):
        return # Silently fail if no credentials

    try:
        yag = yagmail.SMTP(email_user, email_password)
        subject = f"✅ Successfully Published to {platform}: {topic}"
        body = f"""Hello,\n\nA new video has been successfully published to {platform}.\n\nTopic: {topic}\nTimestamp: {datetime.now().isoformat()}\n\n- The Autonomous System"""
        yag.send(to=email_to, subject=subject, contents=body)
        print(f"Successfully sent {platform} success notification email.")
    except Exception as e:
        print(f"Failed to send success notification email: {e}")
