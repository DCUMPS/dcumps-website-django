from django.contrib.sitemaps import Sitemap
from .models import Post
from django.urls import reverse
import datetime

class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9
    protocol = 'https'

    def items(self):
        return Post.objects.all().order_by("-created_on")

    def lastmod(self, obj):
        return obj.last_modified
    
class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'daily'
    protocol = 'https'

    def items(self):
        return ['index', 'links', 'links_tv', 'links_tcv', 'links_fm', 'committee', 'contact', 'dcutv', 'gallery', 'swapweek', 'memes', 'dcufm']

    def location(self, item):
        return reverse(item)
    
    def lastmod(self, obj):
        return datetime.datetime.now()