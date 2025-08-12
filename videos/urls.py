# urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.videos_list, name='videos_list'),
    path('playlists/', views.playlists_list, name='playlists_list'),
    path('playlist/<int:playlist_id>/', views.playlist_detail, name='playlist_detail'),
    path('<int:video_id>/', views.video_detail, name='video_detail'),
    path('<int:video_id>/page/<int:page_number>/', views.video_detail, name='video_detail_page'),
    path('categories/<slug:slug>/videos/', views.videos_by_category, name='videos_by_category'),
    path('categories/<slug:slug>/playlists/', views.playlists_by_category, name='playlists_by_category'),
]