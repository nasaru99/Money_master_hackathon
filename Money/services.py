# youtube_app/services.py

from googleapiclient.discovery import build
from django.conf import settings

def get_youtube_service():
    return build('youtube', 'v3', developerKey=settings.YOUTUBE_API_KEY)

def search_youtube(query):
    youtube = get_youtube_service()
    request = youtube.search().list(q=query, part='id,snippet', maxResults=10)
    response = request.execute()
    return response['items']
