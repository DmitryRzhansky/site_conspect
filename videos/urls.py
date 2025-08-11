from django.urls import path
from . import views

urlpatterns = [
    path('', views.videos_list, name='videos_list'),  # список всех видео
    path('playlists/', views.playlists_list, name='playlists_list'),  # список всех плейлистов
    path('playlist/<int:playlist_id>/', views.playlist_detail, name='playlist_detail'),  # страница одного плейлиста с видео
    path('<int:video_id>/', views.video_detail, name='video_detail'),
    path('<int:video_id>/page/<int:page_number>/', views.video_detail, name='video_detail_page'),
]
