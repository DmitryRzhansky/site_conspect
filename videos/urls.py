from django.urls import path
from . import views

urlpatterns = [
    path('', views.videos_list, name='videos_list'),
    path('<int:video_id>/', views.video_detail, name='video_detail'),
    path('<int:video_id>/page/<int:page_number>/', views.video_detail, name='video_detail_page'),
]