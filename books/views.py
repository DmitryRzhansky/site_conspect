from django.shortcuts import render, get_object_or_404
from .models import Book, Chapter

from django.core.paginator import Paginator


def books_list(request):
    books_list = Book.objects.all()
    paginator = Paginator(books_list, 5)  # Показывать по 5 книг на страницу

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'books/books_list.html', {'page_obj': page_obj})

def chapter_detail(request, book_id, chapter_number):
    book = get_object_or_404(Book, pk=book_id)
    chapter = get_object_or_404(Chapter, book=book, number=chapter_number)
    return render(request, 'books/chapter_detail.html', {'book': book, 'chapter': chapter})
