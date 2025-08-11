from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    cover = models.ImageField(upload_to='book_covers/', blank=True, null=True)
    description = models.TextField(blank=True)               # Описание книги
    file = models.FileField(upload_to='book_files/', blank=True, null=True)  # Файл книги для скачивания

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
    page = models.PositiveIntegerField(default=1)  # теперь просто номер страницы для удобства

    def __str__(self):
        return f"Изображение для {self.chapter} - {self.description or 'без описания'}"
