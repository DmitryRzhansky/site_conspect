from django.contrib import admin
from django.forms import Textarea
from django.db import models  # <- вот этот импорт обязателен
from .models import Article

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_date')
    search_fields = ('title', 'author')
    list_filter = ('publication_date',)
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 20, 'cols': 100})},
    }
