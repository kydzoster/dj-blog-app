from django.contrib.sitemaps import Sitemap
from .models import Post

# custom sitemap with change frequency of post pages and their relevance on the website, max is 1
class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9
    # this method returns queryset of objects to include in this sitemap
    def items(self):
        return Post.published.all()
    # returns the last time the object was modified
    def lastmod(self, obj):
        return obj.updated
