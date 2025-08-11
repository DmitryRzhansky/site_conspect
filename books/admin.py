from django.contrib import admin
from django.db import models
from .models import Book, Chapter
from django.forms import Textarea

class ChapterInline(admin.TabularInline):
    model = Chapter
    extra = 1

class BookAdmin(admin.ModelAdmin):
    list_display = ('title',)
    inlines = [ChapterInline]

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):  # НЕ MarkdownxModelAdmin
    list_display = ('book', 'number', 'title')
    list_filter = ('book',)
    ordering = ('book', 'number')

    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':10, 'cols':80})},
    }

admin.site.register(Book, BookAdmin)
