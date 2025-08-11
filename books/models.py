from django.db import models
from django.utils.text import slugify


class Book(models.Model):
    title = models.CharField(max_length=200)
    cover = models.ImageField(upload_to='book_covers/', blank=True, null=True)
    description = models.TextField(blank=True)
    file = models.FileField(upload_to='book_files/', blank=True, null=True)

    # Новые поля
    isbn = models.CharField(max_length=50, blank=True)
    pages_count = models.PositiveIntegerField(blank=True, null=True)
    publication_date = models.DateField(blank=True, null=True)
    format = models.CharField(max_length=50, blank=True)
    publisher = models.CharField(max_length=100, blank=True)
    language = models.CharField(max_length=50, blank=True)
    author = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.title


class Chapter(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='chapters')
    number = models.PositiveIntegerField()
    title = models.CharField(max_length=200)
    content = models.TextField(blank=True)

    class Meta:
        unique_together = ('book', 'number')
        ordering = ['number']

    def __str__(self):
        return f"Глава {self.number}: {self.title}"


class ChapterImage(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='chapter_images/')
    description = models.CharField(max_length=255, blank=True)
    page = models.PositiveIntegerField(default=1)  # номер страницы для удобства

    def __str__(self):
        return f"Изображение для {self.chapter} - {self.description or 'без описания'}"

class Term(models.Model):
    name = models.CharField(max_length=100, unique=True)
    definition = models.TextField()
    slug = models.SlugField(max_length=120, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name