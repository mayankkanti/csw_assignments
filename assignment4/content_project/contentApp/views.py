from django.shortcuts import render, get_object_or_404
from .models import Article
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.db import connection


def article_list(request):
    articles = Article.published.all()
    paginator = Paginator(articles, 5)
    page = request.GET.get('page')
    articles_page = paginator.get_page(page)
    return render(request, 'contentApp/list.html', {'articles': articles_page, 'paginator': paginator})


def article_detail(request, year, month, day, slug):
    article = get_object_or_404(
        Article,
        status=Article.Status.PUBLISHED,
        slug=slug,
        publish__year=year,
        publish__month=month,
        publish__day=day
    )
    tag_ids = article.tags.values_list('id', flat=True)
    similar = Article.published.filter(tags__in=tag_ids).exclude(id=article.id)
    similar = similar.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:3]
    return render(request, 'contentApp/detail.html', {'article': article, 'similar': similar})


def article_search(request):
    query = request.GET.get('q', '')
    results = Article.published.none()
    if query:
        if connection.vendor == 'postgresql':
            from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
            vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
            search_q = SearchQuery(query)
            results = Article.published.annotate(
                rank=SearchRank(vector, search_q)
            ).filter(rank__gte=0.1).order_by('-rank')
        else:
            results = Article.published.filter(
                Q(title__icontains=query) | Q(body__icontains=query)
            ).order_by('-publish')
    paginator = Paginator(results, 5)
    page = request.GET.get('page')
    articles = paginator.get_page(page)
    return render(request, 'contentApp/search.html', {'articles': articles, 'paginator': paginator, 'query': query})
