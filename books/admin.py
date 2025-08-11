from django.contrib import admin
from django.forms import Textarea
from django.db import models
from .models import Book, Chapter, ChapterImage

class ChapterImageInline(admin.TabularInline):
    model = ChapterImage
    extra = 1
    fields = ('image', 'description', 'page')
    # Чтобы удобно назначать номер страницы прямо в админке

class ChapterInline(admin.TabularInline):
    model = Chapter
    extra = 1

class BookAdmin(admin.ModelAdmin):
    list_display = ('title',)
    inlines = [ChapterInline]

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ('book', 'number', 'title')
    list_filter = ('book',)
    ordering = ('book', 'number')
    inlines = [ChapterImageInline]
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 15, 'cols': 100})},
    }

admin.site.register(Book, BookAdmin)
