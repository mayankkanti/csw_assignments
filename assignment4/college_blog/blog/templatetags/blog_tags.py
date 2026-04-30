from django import template
from django.template.loader import render_to_string
from ..models import Post
from django.db.models import Count

register = template.Library()


@register.simple_tag
def total_posts():
    return Post.published.count()


@register.inclusion_tag('blog/post/latest_posts.html')
def latest_posts(count=5):
    posts = Post.published.order_by('-publish')[:count]
    return {'latest_posts': posts}


@register.inclusion_tag('blog/post/most_commented.html')
def most_commented(count=5):
    posts = Post.published.annotate(comment_count=Count('comments')).order_by('-comment_count')[:count]
    return {'most_commented_posts': posts}


@register.filter(name='markdown')
def markdown_format(text):
    if not text:
        return ''
    try:
        import markdown as _markdown
        from django.utils.safestring import mark_safe
        return mark_safe(_markdown.markdown(text))
    except Exception:
        return text
