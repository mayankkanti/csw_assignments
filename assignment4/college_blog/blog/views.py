from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .models import Post

from django.core.mail import send_mail
from .forms import EmailPostForm, CommentForm
from django.core.paginator import Paginator
from taggit.models import Tag
from django.db.models import Count, Q
from django.db import connection
from .feeds import LatestPostsFeed


def post_list(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])
    paginator = Paginator(object_list, 3)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    posts = page_obj.object_list
    return render(request, 'blog/post/list.html', {'posts': posts, 'page_obj': page_obj, 'paginator': paginator, 'tag': tag})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        status=Post.Status.PUBLISHED,
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day
    )
    comments = post.comments.filter(active=True)
    form = CommentForm()
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]
    return render(request, 'blog/post/detail.html', {'post': post, 'comments': comments, 'form': form, 'similar_posts': similar_posts})

def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = f"Read {post.title} at {post_url}\n\n{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, cd['email'], [cd['to']])
            sent = True
    else:
        form = EmailPostForm()
    return render(request, 'blog/post/share.html', {'post': post, 'form': form, 'sent': sent})

def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    if request.method == 'POST':
        form = CommentForm(data=request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
    else:
        form = CommentForm()
    return render(request, 'blog/post/comment.html', {'post': post, 'form': form, 'comment': comment})


def post_search(request):
    query = request.GET.get('q', '')
    results = Post.published.none()
    if query:
        if connection.vendor == 'postgresql':
            from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
            vector = SearchVector('title', weight='A') + SearchVector('body', weight='B')
            search_q = SearchQuery(query)
            results = Post.published.annotate(
                rank=SearchRank(vector, search_q)
            ).filter(rank__gte=0.1).order_by('-rank')
        else:
            results = Post.published.filter(
                Q(title__icontains=query) | Q(body__icontains=query)
            ).order_by('-publish')
    paginator = Paginator(results, 5)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)
    return render(request, 'blog/post/search.html', {'results': page_obj.object_list, 'page_obj': page_obj, 'query': query})


def feed_response(request):
    response = LatestPostsFeed()(request)
    response['Content-Type'] = 'application/xml; charset=utf-8'
    response['Content-Disposition'] = 'inline; filename="feed.xml"'
    return response