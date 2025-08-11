from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Video

def videos_list(request):
    videos = Video.objects.all()

    search_query = request.GET.get('search', '').strip()
    author_filter = request.GET.get('author', '').strip()

    if search_query:
        videos = videos.filter(title__icontains=search_query)

    if author_filter:
        videos = videos.filter(author__icontains=author_filter)

    paginator = Paginator(videos, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'videos/videos_list.html', {
        'page_obj': page_obj,
        'search_query': search_query,
        'author_filter': author_filter,
    })

def video_detail(request, video_id, page_number=1):
    video = get_object_or_404(Video, pk=video_id)
    content = video.transcript or ''

    max_chars = 4000  # макс символов на страницу

    blocks = split_markdown_blocks(content)

    pages = []
    current_text = ''
    current_len = 0

    for block in blocks:
        block_len = len(block) + 2
        if current_len + block_len <= max_chars:
            current_text += block + '\n\n'
            current_len += block_len
        else:
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

    return render(request, 'videos/video_detail.html', {
        'video': video,
        'page_obj': page_obj,
    })
def split_markdown_blocks(text, max_block_lines=20):
    import re
    blocks = []
    code_pattern = re.compile(r'(```[\s\S]+?```)', re.MULTILINE)
    last_pos = 0

    for match in code_pattern.finditer(text):
        # Добавляем текст до код-блока
        if match.start() > last_pos:
            pre_text = text[last_pos:match.start()]
            para_blocks = [b.strip() for b in pre_text.split('\n\n') if b.strip()]
            blocks.extend(para_blocks)

        # Добавляем код-блок, разбивая его, если длинный
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

    # Остаток текста после последнего код-блока
    if last_pos < len(text):
        rest_text = text[last_pos:]
        para_blocks = [b.strip() for b in rest_text.split('\n\n') if b.strip()]
        blocks.extend(para_blocks)

    return blocks

