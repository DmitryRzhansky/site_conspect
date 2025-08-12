from django.shortcuts import render
from .models import Article
from django.core.paginator import Paginator

def article_list(request):
    articles = Article.objects.all().order_by('-publication_date')

    search_query = request.GET.get('search', '').strip()
    if search_query:
        articles = articles.filter(title__icontains=search_query)

    paginator = Paginator(articles, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'articles/article_list.html', {'page_obj': page_obj, 'search_query': search_query})
