from django.contrib import admin
from django.urls import include, path
from . import views
from .views import *
from django.views.generic.base import TemplateView
from django.views.generic import RedirectView
import re
from django.conf import settings

urlpatterns = [
    path('', views.index, name="index"),
    path('link', views.links, name="links"),
    path('links', views.links, name="links"),
    path('linktree', views.links, name="links"),
    path('linksdcutv', views.links_tv, name="links_tv"),
    path('linkstcv', views.links_tcv, name="links_tcv"),
    path('linksdcufm', views.links_fm, name="links_fm"),
    path('linksthedev', views.links_dev, name="links_dev"),
    path('committee', views.committee, name="committee"),
    path('contact', views.contact, name="contact"),
    path('dcutv', views.dcutv, name="dcutv"),
    path('gallery', views.gallery, name="gallery"),
    path("swapweek", views.swapweek, name="swapweek"),
    path("memes", views.memes, name="memes"),
    path("dcufm", views.dcufm, name="dcufm"),
    path("thedev", views.thedev, name="thedev"),
    path("loans", views.loans, name="loans"),
    path("ads", views.ads, name="ads"),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type='text/plain')),
    path('favicon.ico', RedirectView.as_view(url=settings.STATIC_URL + 'assets/img/other/favicon.ico')),
    path('donate', RedirectView.as_view(url="https://www.idonate.ie/fundraiser/MediaProductionSociety13"), name="donate"),
    path('lounge', RedirectView.as_view(url="https://lounge.live/lounges/kr53i9b6"), name="lounge"),
    path('join', RedirectView.as_view(url="https://dcuclubsandsocs.ie/society/media-production"), name="join"),
    path('thinktank', RedirectView.as_view(url="https://chat.whatsapp.com/EBupVbTpWX01uJvBp5r24D"), name="thinktank"),
    path('tcv', RedirectView.as_view(url="https://www.thecollegeview.ie"), name="tcv"),
    path('youtube', RedirectView.as_view(url="https://youtube.com/dcumps"), name="youtube"),
    path('tiktok', RedirectView.as_view(url="https://www.tiktok.com/@dcumps"), name="tiktok"),
    path('instagram', RedirectView.as_view(url="https://instagram.com/dcumps"), name="instagram"),
    path('facebook', RedirectView.as_view(url="https://facebook.com/dcumps"), name="facebook"),
    path('twitter', RedirectView.as_view(url="https://twitter.com/dcumps"), name="twitter"),
    path('twitch', RedirectView.as_view(url="https://twitch.tv/dcufm"), name="twitch"),
    path('broadcast', RedirectView.as_view(url="https://youtube.com/dcumps"), name="broadcast"),
    path('page-not-found', views.page_not_found, name="404"),
    path("blog", views.blog_index, name="blog_index"),
    path('blog/post/<slug:slug>/', blog_detail, name='blog_detail'),
    path("blog/category/<category>/", views.blog_category, name="blog_category"),
    path("blog/author/<author>/", views.blog_author, name="blog_author"),
    path("committee/history", views.committee_history, name="committee_history"),
    path("committee/<slug:year>/", views.committee_history_detail, name="committee_history_detail"),
    path("thecollegeview", views.tcv, name="tcv"),
    path("history", views.history, name="history"),
]