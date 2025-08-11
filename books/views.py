from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import Book, Chapter


def books_list(request):
    books = Book.objects.all()
    paginator = Paginator(books, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'books/books_list.html', {'page_obj': page_obj})

def split_markdown_blocks(text, max_block_lines=20):
    """
    Разбиваем markdown на блоки:
    - Обычный текст по параграфам (\n\n)
    - Кодовые блоки ```...``` разбиваем на части по max_block_lines строк, если они слишком длинные
    """
    import re
    blocks = []
    code_pattern = re.compile(r'(```[\s\S]+?```)', re.MULTILINE)
    last_pos = 0

    for match in code_pattern.finditer(text):
        # Текст перед кодом
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

    # Текст после последнего кода
    if last_pos < len(text):
        rest_text = text[last_pos:]
        para_blocks = [b.strip() for b in rest_text.split('\n\n') if b.strip()]
        blocks.extend(para_blocks)

    return blocks

def chapter_detail(request, book_id, chapter_number, page_number=1):
    book = get_object_or_404(Book, pk=book_id)
    chapter = get_object_or_404(Chapter, book=book, number=chapter_number)
    content = chapter.content or ''

    max_chars = 4000  # макс символов на страницу, можно подкорректировать

    blocks = split_markdown_blocks(content)

    pages = []
    current_text = ''
    current_len = 0
    page_blocks = []

    for block in blocks:
        block_len = len(block) + 2  # учитываем отступы и переносы
        if current_len + block_len <= max_chars:
            current_text += block + '\n\n'
            current_len += block_len
            page_blocks.append(block)
        else:
            pages.append(current_text.strip())
            current_text = block + '\n\n'
            current_len = block_len
            page_blocks = [block]

    if current_text:
        pages.append(current_text.strip())

    if not pages:
        pages = ['']

    if page_number < 1 or page_number > len(pages):
        page_number = 1

    page_text = pages[page_number - 1]

    # Изображения на странице — фильтрация по полю page
    images_on_page = chapter.images.filter(page=page_number).order_by('id')

    class PageObj:
        def __init__(self, number, num_pages):
            self.number = number
            self.paginator = type('Paginator', (), {'num_pages': num_pages})()
            self.object_list = [page_text]
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
