# articles/admin.py
from django.contrib import admin
from django.forms import Textarea
from django.db import models
from .models import Article, Category

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_date')
    search_fields = ('title', 'author', 'content')
    list_filter = ('publication_date', 'categories')
    filter_horizontal = ('categories',)
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 20, 'cols': 100})},
    }

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}