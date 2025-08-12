# articles/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.article_list, name='article_list'),
    path('categories/<slug:slug>/', views.articles_by_category, name='articles_by_category'),
]