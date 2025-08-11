from django.contrib import admin
from django.forms import Textarea
from django.db import models
from .models import Book, Chapter, ChapterImage

class ChapterImageInline(admin.TabularInline):
    model = ChapterImage
    extra = 1
    fields = ('image', 'description', 'page')

class ChapterInline(admin.TabularInline):
    model = Chapter
    extra = 1

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publisher', 'publication_date')
    search_fields = ('title', 'author', 'publisher', 'isbn')
    list_filter = ('language', 'publisher', 'publication_date')
    inlines = [ChapterInline]
    fields = (
        'title', 'author', 'publisher', 'publication_date',
        'isbn', 'pages_count', 'format', 'language',
        'cover', 'description', 'file'
    )

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('book', 'number', 'title')
    list_filter = ('book',)
    ordering = ('book', 'number')
    inlines = [ChapterImageInline]
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 15, 'cols': 100})},
    }
