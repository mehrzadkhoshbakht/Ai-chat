import os
import yagmail
from datetime import datetime

def send_error_notification(error_message, traceback_info):
    """Sends an email notification when a critical error occurs."""

    email_user = os.environ.get("EMAIL_USER")
    email_password = os.environ.get("EMAIL_PASSWORD")
    email_to = os.environ.get("EMAIL_TO")

    if not all([email_user, email_password, email_to]):
        print("Email credentials not found in environment variables. Cannot send error notification.")
        return

    try:
        yag = yagmail.SMTP(email_user, email_password)

        subject = f"🚨 Critical Error in Zero-Touch MikroTik Factory"

        body = f"""
        Hello,

        A critical error occurred in the content creation pipeline at {datetime.now().isoformat()}.

        Error Message:
        {error_message}

        Traceback:
        <pre>
        {traceback_info}
        </pre>

        Please check the system logs for more details.

        - The Autonomous System
        """

        yag.send(
            to=email_to,
            subject=subject,
            contents=body
        )
        print("Successfully sent error notification email.")

    except Exception as e:
        print(f"Failed to send error notification email: {e}")
