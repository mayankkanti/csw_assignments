from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models import Post


class LatestPostsFeed(Feed):
    title = "Blog Posts"
    link = "/"
    description = "Latest blog posts"
    content_type = 'application/xml; charset=utf-8'

    def items(self):
        return Post.published.order_by('-publish')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.body

    def item_link(self, item):
        return item.get_absolute_url()

    def item_pubdate(self, item):
        return item.publish
