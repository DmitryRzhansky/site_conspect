# articles/views.py
from django.shortcuts import render, get_object_or_404
from .models import Article, Category
from django.core.paginator import Paginator

def article_list(request):
    articles = Article.objects.all().order_by('-publication_date')
    categories = Category.objects.all()
    
    search_query = request.GET.get('search', '').strip()
    category_filter = request.GET.get('category', '').strip()
    
    if search_query:
        articles = articles.filter(title__icontains=search_query)
    
    if category_filter:
        articles = articles.filter(categories__name__icontains=category_filter)
    
    paginator = Paginator(articles, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
        'category_filter': category_filter,
        'categories': categories,
    }
    return render(request, 'articles/article_list.html', context)

def articles_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    articles = category.articles.all().order_by('-publication_date')
    
    paginator = Paginator(articles, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, 'articles/articles_by_category.html', context)