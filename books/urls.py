from django.urls import path
from . import views

urlpatterns = [
    path('', views.books_list, name='books_list'),
    path('<int:book_id>/chapter/<int:chapter_number>/', views.chapter_detail, name='chapter_detail'),
    path('<int:book_id>/chapter/<int:chapter_number>/page/<int:page_number>/', views.chapter_detail, name='chapter_detail_page'),
]