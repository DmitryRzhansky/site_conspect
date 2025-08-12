
from django.shortcuts import render, get_object_or_404
from .models import Book, Chapter, Term, Category
from django.core.paginator import Paginator
from django.db.models import Q
from django.urls import reverse
import re

def linkify_terms(text, terms):
    if not terms:
        return text

    sorted_terms = sorted(terms, key=lambda t: len(t.name), reverse=True)
    pattern = re.compile('|'.join(re.escape(term.name) for term in sorted_terms), re.IGNORECASE)

    def replacer(match):
        matched_text = match.group(0)
        term_obj = next((t for t in sorted_terms if t.name.lower() == matched_text.lower()), None)
        if term_obj:
            url = reverse('term_detail', args=[term_obj.slug])
            return f'<a href="{url}" class="term-link" title="Посмотреть определение">{matched_text}</a>'
        return matched_text

    return pattern.sub(replacer, text)


def chapter_detail(request, book_id, chapter_number, page_number=1):
    book = get_object_or_404(Book, pk=book_id)
    chapter = get_object_or_404(Chapter, book=book, number=chapter_number)
    content = chapter.content or ''

    max_chars = 4000  # Максимум символов на страницу (можно настраивать)

    # Разбиваем markdown на блоки с учётом кода, чтобы не резать внутри кода
    def split_markdown_blocks(text, max_block_lines=20):
        blocks = []
        code_pattern = re.compile(r'(```[\s\S]+?```)', re.MULTILINE)
        last_pos = 0

        for match in code_pattern.finditer(text):
            if match.start() > last_pos:
                pre_text = text[last_pos:match.start()]
                para_blocks = [b.strip() for b in pre_text.split('\n\n') if b.strip()]
                blocks.extend(para_blocks)

            code_block = match.group()
            code_lines = code_block.split('\n')
            if len(code_lines) > max_block_lines + 2:
                start_marker = code_lines[0]
                end_marker = code_lines[-1]
                code_body = code_lines[1:-1]

                for i in range(0, len(code_body), max_block_lines):
                    part = code_body[i:i+max_block_lines]
                    part_block = '\n'.join([start_marker] + part + [end_marker])
                    blocks.append(part_block)
            else:
                blocks.append(code_block)

            last_pos = match.end()

        if last_pos < len(text):
            rest_text = text[last_pos:]
            para_blocks = [b.strip() for b in rest_text.split('\n\n') if b.strip()]
            blocks.extend(para_blocks)

        return blocks

    blocks = split_markdown_blocks(content)

    pages = []
    current_text = ''
    current_len = 0

    for block in blocks:
        block_len = len(block) + 2  # +2 для переносов строк
        if current_len + block_len <= max_chars:
            current_text += block + '\n\n'
            current_len += block_len
        else:
            if current_text:
                pages.append(current_text.strip())
            current_text = block + '\n\n'
            current_len = block_len

    if current_text:
        pages.append(current_text.strip())

    if not pages:
        pages = ['']

    if page_number < 1 or page_number > len(pages):
        page_number = 1

    page_text = pages[page_number - 1]

    terms = list(Term.objects.all())

    linked_text = linkify_terms(page_text, terms)

    images_on_page = chapter.images.filter(page=page_number).order_by('id')

    class PageObj:
        def __init__(self, number, num_pages):
            self.number = number
            self.paginator = type('Paginator', (), {'num_pages': num_pages})()
            self.object_list = [linked_text]
            self.has_previous = number > 1
            self.has_next = number < num_pages
            self.previous_page_number = number - 1
            self.next_page_number = number + 1

    page_obj = PageObj(page_number, len(pages))

    return render(request, 'books/chapter_detail.html', {
        'book': book,
        'chapter': chapter,
        'page_obj': page_obj,
        'images_on_page': images_on_page,
    })


def terms_list(request):
    terms = Term.objects.all().order_by('name')
    categories = Category.objects.all()
    
    search_query = request.GET.get('search', '').strip()
    category_filter = request.GET.get('category', '').strip()
    
    if search_query:
        terms = terms.filter(
            Q(name__icontains=search_query) | 
            Q(definition__icontains=search_query)
        )
    
    if category_filter:
        terms = terms.filter(categories__name__icontains=category_filter)
    
    paginator = Paginator(terms, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'search_query': search_query,
        'category_filter': category_filter,
    }
    return render(request, 'books/terms_list.html', context)

def books_list(request):
    books = Book.objects.all().order_by('-publication_date')
    categories = Category.objects.all()
    
    search_query = request.GET.get('search', '').strip()
    author_filter = request.GET.get('author', '').strip()
    language_filter = request.GET.get('language', '').strip()
    publisher_filter = request.GET.get('publisher', '').strip()
    category_filter = request.GET.get('category', '').strip()
    
    if search_query:
        books = books.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    if author_filter:
        books = books.filter(author__icontains=author_filter)
    
    if language_filter:
        books = books.filter(language__icontains=language_filter)
    
    if publisher_filter:
        books = books.filter(publisher__icontains=publisher_filter)
    
    if category_filter:
        books = books.filter(category__name__icontains=category_filter)
    
    paginator = Paginator(books, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'search_query': search_query,
        'author_filter': author_filter,
        'language_filter': language_filter,
        'publisher_filter': publisher_filter,
        'category_filter': category_filter,
    }
    return render(request, 'books/books_list.html', context)


def slugify_term(name):
    slug = name.lower()
    slug = re.sub(r'[^\w]+', '-', slug)
    slug = slug.strip('-')
    return slug

def term_detail(request, slug):
    term = get_object_or_404(Term, slug=slug)
    return render(request, 'books/term_detail.html', {'term': term})

def categories_list(request):
    categories = Category.objects.all()
    return render(request, 'books/categories_list.html', {'categories': categories})

def books_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    books = category.books.all().order_by('-publication_date')
    
    search_query = request.GET.get('search', '').strip()
    if search_query:
        books = books.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query)
        )
    
    paginator = Paginator(books, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
        'search_query': search_query,
    }
    return render(request, 'books/books_by_category.html', context)

def terms_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    terms = category.terms.all().order_by('name')
    
    search_query = request.GET.get('search', '').strip()
    if search_query:
        terms = terms.filter(
            Q(name__icontains=search_query) | 
            Q(definition__icontains=search_query)
        )
    
    paginator = Paginator(terms, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
        'search_query': search_query,
    }
    return render(request, 'books/terms_by_category.html', context)