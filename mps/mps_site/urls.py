from django.contrib import admin
from django.urls import include, path
from . import views
from .views import *
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap
from django.views.generic.base import TemplateView

sitemaps = {
    "static": StaticViewSitemap,
}


urlpatterns = [
    path('', views.index, name="index"),
    path('links', views.links, name="links"),
    path('linksdcutv', views.links_tv, name="links_tv"),
    path('linkstcv', views.links_tcv, name="links_tcv"),
    path('linksdcufm', views.links_fm, name="links_fm"),
    path('committee', views.committee, name="committee"),
    path('contact', views.contact, name="contact"),
    path('dcutv', views.dcutv, name="dcutv"),
    path('gallery', views.gallery, name="gallery"),
    #path('blog', views.blog, name="blog"),
    #path('merch', views.merch, name="merch"),
    #path("admin/", admin.site.urls),
    #path("comingsoon", views.comingsoon, name="comingsoon"),
    path("swapweek", views.swapweek, name="swapweek"),
    path("memes", views.memes, name="memes"),
    path("dcufm", views.dcufm, name="dcufm"),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
    ),
    path('donate', views.donate, name="donate"),
    path('lounge', views.lounge, name="lounge"),
    path('join', views.join, name="join"),
    path('thinktank', views.thinktank, name="thinktank"),
    path('tcv', views.tcv, name="tcv"),
    path('youtube', views.youtube, name="youtube"),
    path('tiktok', views.tiktok, name="tiktok"),
    path('instagram', views.instagram, name="instagram"),
    path('facebook', views.facebook, name="facebook"),
    path('twitter', views.twitter, name="twitter"),
    path('twitch', views.twitch, name="twitch"),
    path('broadcast', views.broadcast, name="broadcast"),
]