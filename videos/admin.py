# admin.py
from django.contrib import admin
from .models import Video, Playlist, Category

class VideoInline(admin.TabularInline):
    model = Video
    extra = 0
    fields = ('title', 'author', 'youtube_url', 'playlist', 'category')

@admin.register(Playlist)
class PlaylistAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'description')
    inlines = [VideoInline]

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'playlist', 'category', 'created_at')
    search_fields = ('title', 'author', 'description')
    list_filter = ('author', 'playlist', 'category', 'created_at')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}