from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=200)
    cover = models.ImageField(upload_to='book_covers/', blank=True, null=True)  # поле для обложки книги

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
