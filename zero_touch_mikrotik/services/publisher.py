import json
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

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

def publish_content(video_path, topic, subtitle_paths):
    """
    Publishes the video to YouTube.
    """
    print("Publishing content to YouTube...")

    try:
        youtube = get_youtube_service()
    except FileNotFoundError as e:
        print(f"Could not initialize YouTube service: {e}")
        print("Skipping YouTube publishing.")
        return False

    with open("zero_touch_mikrotik/config/hashtags.json", "r") as f:
        hashtags = json.load(f)

    title = f"آموزش میکروتیک: {topic}"
    description = f"در این ویدیو به آموزش {topic} می‌پردازیم.\n\n" + " ".join(hashtags)
    tags = ["MikroTik", "tutorial", "Persian"] + [tag.strip('#') for tag in hashtags]

    request_body = {
        'snippet': {
            'categoryId': '28', # Science & Technology
            'title': title,
            'description': description,
            'tags': tags,
            'defaultLanguage': 'fa',
            'defaultAudioLanguage': 'fa'
        },
        'status': {
            'privacyStatus': 'private', # 'private', 'public', or 'unlisted'
            'selfDeclaredMadeForKids': False,
        }
    }

    media = MediaFileUpload(video_path, chunksize=-1, resumable=True)

    print("Uploading video to YouTube...")
    response_upload = youtube.videos().insert(
        part='snippet,status',
        body=request_body,
        media_body=media
    ).execute()

    video_id = response_upload.get('id')
    if video_id:
        print(f"Video uploaded successfully! Video ID: {video_id}")

        # Upload Farsi subtitles
        srt_path_fa = next((s for s in subtitle_paths if s.endswith("_fa.srt")), None)
        if srt_path_fa:
            print("Uploading Farsi subtitles...")
            youtube.captions().insert(
                part='snippet',
                body={
                    'snippet': {
                        'videoId': video_id,
                        'language': 'fa',
                        'name': 'Farsi',
                        'isDraft': False
                    }
                },
                media_body=MediaFileUpload(srt_path_fa)
            ).execute()
            print("Subtitles uploaded.")
    else:
        print("Could not get video ID after upload.")
        return False

    print("Publishing complete.")
    return True
