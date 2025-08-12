from django.urls import path
from . import views

urlpatterns = [
    path('', views.books_list, name='books_list'),
    path('<int:book_id>/chapter/<int:chapter_number>/', views.chapter_detail, name='chapter_detail'),
    path('<int:book_id>/chapter/<int:chapter_number>/page/<int:page_number>/', views.chapter_detail, name='chapter_detail_page'),
    path('terms/', views.terms_list, name='terms_list'),
    path('term/<slug:slug>/', views.term_detail, name='term_detail'),
    path('categories/', views.categories_list, name='categories_list'),
    path('category/<slug:slug>/', views.books_by_category, name='books_by_category'),
    path('terms/category/<slug:slug>/', views.terms_by_category, name='terms_by_category'),
]