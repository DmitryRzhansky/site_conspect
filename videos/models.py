from django.db import models
from urllib.parse import urlparse, parse_qs

class Playlist(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    transcript = models.TextField(blank=True)
    video_file = models.FileField(upload_to='videos/', blank=True, null=True)
    youtube_url = models.URLField(blank=True, null=True)
    thumbnail = models.ImageField(upload_to='video_thumbnails/', blank=True, null=True)
    author = models.CharField(max_length=100, blank=True)
    playlist = models.ForeignKey(Playlist, related_name='videos', on_delete=models.SET_NULL, null=True, blank=True)

    def youtube_id(self):
        if not self.youtube_url:
            return None
        url_data = urlparse(self.youtube_url)
        if url_data.hostname == 'youtu.be':
            return url_data.path[1:]
        if url_data.hostname in ['www.youtube.com', 'youtube.com']:
            query = parse_qs(url_data.query)
            return query.get('v', [None])[0]
        return None

    def __str__(self):
        return self.title
