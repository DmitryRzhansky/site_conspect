from django.contrib import admin
from .models import Video

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'youtube_url', 'video_file')
    search_fields = ('title', 'author')
    list_filter = ('author',)
    readonly_fields = ('youtube_id',)

    def youtube_id(self, obj):
        return obj.youtube_id()
    youtube_id.short_description = "YouTube ID"
