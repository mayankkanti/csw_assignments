from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models import Article


class LatestArticlesFeed(Feed):
    title = "Articles"
    link = "/"
    description = "Latest articles"
    content_type = 'application/xml; charset=utf-8'

    def items(self):
        return Article.published.order_by('-publish')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.body

    def item_link(self, item):
        return item.get_absolute_url()

    def item_pubdate(self, item):
        return item.publish
