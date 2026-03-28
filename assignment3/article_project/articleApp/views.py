from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .forms import ArticleShareForm, CommentForm
from .models import Article


def article_list(request):
    articles = Article.objects.all()
    paginator = Paginator(articles, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'articleApp/article_list.html', {'page_obj': page_obj})


def article_detail(request, year, month, day, article):
    article_obj = get_object_or_404(
        Article,
        slug=article,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
    comments = article_obj.comments.all().order_by('-created')
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article_obj
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(
        request,
        'articleApp/article_detail.html',
        {
            'article': article_obj,
            'comments': comments,
            'new_comment': new_comment,
            'comment_form': comment_form,
        },
    )


def article_share(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    sent = False

    if request.method == 'POST':
        form = ArticleShareForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            article_url = request.build_absolute_uri(
                reverse(
                    'article_detail',
                    args=[article.publish.year, article.publish.month, article.publish.day, article.slug],
                )
            )
            subject = f"{cd['name']} recommends you read {article.title}"
            message = (
                f"Read {article.title} at {article_url}\n\n"
                f"{cd['name']}\'s comments: {cd['comments']}"
            )
            send_mail(subject, message, cd['email'], [cd['recipient_email']])
            sent = True
    else:
        form = ArticleShareForm()

    return render(
        request,
        'articleApp/article_share.html',
        {'article': article, 'form': form, 'sent': sent},
    )
