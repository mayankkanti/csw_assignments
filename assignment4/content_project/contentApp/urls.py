from django.urls import path
from django.views.generic.base import RedirectView
from . import views
from .feeds import LatestArticlesFeed

app_name = 'contentApp'

urlpatterns = [
    path('', views.article_list, name='list'),
    path('search/', views.article_search, name='search'),
    path('feed.xml', LatestArticlesFeed(), name='feed'),
    path('feed/', RedirectView.as_view(url='/feed.xml', permanent=True)),
    path('<int:year>/<int:month>/<int:day>/<slug:slug>/', views.article_detail, name='detail'),
]
