from django.contrib import admin
from django.db import models
from django import forms
from ckeditor.widgets import CKEditorWidget
from .models import Book, Chapter, ChapterImage
from .models import Term


class ChapterImageInline(admin.TabularInline):
    model = ChapterImage
    extra = 1
    fields = ('image', 'description', 'page')

class ChapterInline(admin.TabularInline):
    model = Chapter
    extra = 1

class BookAdminForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget(), required=False)

    class Meta:
        model = Book
        fields = '__all__'

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    form = BookAdminForm
    list_display = ('title', 'author', 'publisher', 'publication_date')
    search_fields = ('title', 'author', 'publisher', 'isbn')
    list_filter = ('language', 'publisher', 'publication_date')
    inlines = [ChapterInline]
    fields = (
        'title', 'author', 'publisher', 'publication_date',
        'isbn', 'pages_count', 'format', 'language',
        'cover', 'description', 'file'
    )

class ChapterAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget(), required=False)

    class Meta:
        model = Chapter
        fields = '__all__'

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    form = ChapterAdminForm
    list_display = ('book', 'number', 'title')
    list_filter = ('book',)
    ordering = ('book', 'number')
    inlines = [ChapterImageInline]

@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'definition')
    prepopulated_fields = {'slug': ('name',)}