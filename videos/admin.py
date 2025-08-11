from django.contrib import admin
from .models import Video, Playlist

class VideoInline(admin.TabularInline):
    model = Video
    extra = 0

@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    inlines = [VideoInline]

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'youtube_url', 'video_file', 'youtube_id_display')
    search_fields = ('title', 'author')
    list_filter = ('author',)

    def youtube_id_display(self, obj):
        return obj.youtube_id()
    youtube_id_display.short_description = "YouTube ID"
