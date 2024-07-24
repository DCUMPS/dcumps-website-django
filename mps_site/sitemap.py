from django.contrib.sitemaps import Sitemap
from .models import *
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
    
class AuthorSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8
    protocol = 'https'

    def items(self):
        return Author.objects.all().order_by("-name")

    def lastmod(self, obj):
        return datetime.datetime.now()

class CategorySitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8
    protocol = 'https'

    def items(self):
        return Category.objects.all().order_by("-name")

    def lastmod(self, obj):
        return datetime.datetime.now()
    
class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = 'daily'
    protocol = 'https'

    def items(self):
        return ['index', 'links', 'links_tv', 'links_tcv', 'links_fm', 'committee', 'contact', 'dcutv', 'gallery', 'swapweek', 'memes', 'dcufm', 'blog_index', 'committee_history']

    def location(self, item):
        return reverse(item)
    
    def lastmod(self, obj):
        return datetime.datetime.now()