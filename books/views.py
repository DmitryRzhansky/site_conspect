from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Book, Chapter
import re

def split_content_to_pages(text, max_chars=4000):
    paragraphs = text.split('\n\n')
    pages = []
    current_page = ''

    for p in paragraphs:
        if len(current_page) + len(p) + 2 <= max_chars:
            current_page += p + '\n\n'
        else:
            pages.append(current_page.strip())
            current_page = p + '\n\n'
    if current_page:
        pages.append(current_page.strip())
    return pages

def books_list(request):
    books_list = Book.objects.all()
    paginator = Paginator(books_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'books/books_list.html', {'page_obj': page_obj})
def chapter_detail(request, book_id, chapter_number, page_number=1):
    book = get_object_or_404(Book, pk=book_id)
    chapter = get_object_or_404(Chapter, book=book, number=chapter_number)

    content = chapter.content

    # Разбиваем по примерно 3000 символов
    chunk_size = 3000
    parts = [content[i:i + chunk_size] for i in range(0, len(content), chunk_size)]

    paginator = Paginator(parts, 1)  # одна часть — одна страница
    page_obj = paginator.get_page(page_number)

    return render(request, 'books/chapter_detail.html', {
        'book': book,
        'chapter': chapter,
        'page_obj': page_obj,
        'page_number': page_number,
        'num_pages': paginator.num_pages,
        'chapter_number': chapter_number,
    })