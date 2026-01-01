import os
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from django.conf import settings
from .models import YouTubeToken

# Scopes needed for YouTube upload
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def get_flow():
    client_secrets_file = os.path.join(settings.BASE_DIR, 'client_secrets.json')
    flow = google_auth_oauthlib.flow.Flow.from_client_secrets_file(
        client_secrets_file,
        scopes=SCOPES,
        redirect_uri=settings.YOUTUBE_REDIRECT_URI
    )
    return flow

def get_youtube_client():
    token_obj = YouTubeToken.objects.last()
    if not token_obj:
        return None
    
    credentials = google.oauth2.credentials.Credentials(**token_obj.token)
    
    # Check if we need to refresh (client-side simple check, better handled by library)
    # The dictionary 'token' expected by Credentials(**token) usually has everything
    
    youtube = build('youtube', 'v3', credentials=credentials)
    return youtube

def upload_video(youtube, video_path, title, description, category_id="28", privacy_status="unlisted"):
    """
    Uploads a video to YouTube.
    category_id "28" is Science & Technology.
    """
    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': ['noticias', 'ia', 'ciencias'],
            'categoryId': category_id
        },
        'status': {
            'privacyStatus': privacy_status
        }
    }

    media = MediaFileUpload(
        video_path,
        chunksize=1024*1024,
        resumable=True
    )

    request = youtube.videos().insert(
        part=','.join(body.keys()),
        body=body,
        media_body=media
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
             print(f"Uploaded {int(status.progress() * 100)}%")
    
    return response
