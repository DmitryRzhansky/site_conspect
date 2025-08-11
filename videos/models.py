from django.db import models
from urllib.parse import urlparse, parse_qs


class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    transcript = models.TextField(blank=True)
    video_file = models.FileField(upload_to='videos/', blank=True, null=True)  # можно оставить, если захочешь загружать локально
    youtube_url = models.URLField(blank=True, null=True)  # <--- новая ссылка на ютуб
    thumbnail = models.ImageField(upload_to='video_thumbnails/', blank=True, null=True)
    author = models.CharField(max_length=100, blank=True)

    def youtube_id(self):
        if not self.youtube_url:
            return None
        url_data = urlparse(self.youtube_url)
        if url_data.hostname in ['youtu.be']:
            return url_data.path[1:]
        if url_data.hostname in ['www.youtube.com', 'youtube.com']:
            query = parse_qs(url_data.query)
            return query.get('v', [None])[0]
        return None