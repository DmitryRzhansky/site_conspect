from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=300)
    source_url = models.URLField(unique=True)  # ссылка на оригинал
    author = models.CharField(max_length=150, blank=True)
    publication_date = models.DateField(blank=True, null=True)
    content = models.TextField(blank=True)  # конспект статьи в markdown или html
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
