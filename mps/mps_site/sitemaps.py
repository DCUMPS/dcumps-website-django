from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import timezone


class StaticViewSitemap(Sitemap):
    changefreq = "daily"

    def items(self):
        return ["index", "links", "links_tv", "links_tcv", "committee", "contact", "dcutv", "gallery", "dcufm"]

    def location(self, item):
        return reverse(item)
    
    def lastmod(self, item):
        return timezone.now()
    
    def priority(self, item):
        return {'home': 1.0, 'links' : 0.8, "links_tv" : 0.8 , "links_tcv": 0.8 , "committee": 0.8 , "contact": 0.8 , "dcutv": 0.8 , "gallery": 0.8 , "dcufm": 0.8 }[item]
    
