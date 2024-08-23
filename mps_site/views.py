from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import *
from .scripts import *
import json
from django.utils.safestring import mark_safe
from datetime import datetime
import markdown
from .utils import *
from .content import *
from .data.homepage import *
from .data.dcufm import *
from .data.dcutv import *

def render_blog_preview(posts):
    md = markdown.Markdown(extensions=["fenced_code"])
    for post in posts:
        post.body = md.convert(post.body)
        soup = BeautifulSoup(post.body, 'html.parser')
        all_p_tags = soup.find_all('p')
        final = ""
        for p_tag in all_p_tags:
            final += str(p_tag.text) + " "
        final = final.replace("> ", "")
        post.body = final
        post.title = md.convert(post.title)
    return posts
    

def blog_index(request):
    posts = Post.objects.all().order_by("-created_on")
    posts = render_blog_preview(posts)
    
    context = {
        "posts": posts,
        "page_name": "Blog"
    }

    return render(request, "blog/index.html", context)

def blog_category(request, category):
    posts = Post.objects.filter(categories__name__contains=category).order_by("-created_on")
    posts = render_blog_preview(posts)

    context = {
        "category": category,
        "page_name": category,
        "posts": posts,
    }

    return render(request, "blog/category.html", context)

def blog_detail(request, slug):
    post = get_object_or_404(Post, post_slug=slug)
    md = markdown.Markdown(extensions=["fenced_code"])
    post.body = render_markdown(post.body)
    post.title = render_markdown(post.title)  # If necessary, render Markdown for title
    comments = Comment.objects.filter(post=post)
    post_title_text = post.title.replace("<p>", "").replace("</p>", "")
    context = {
        "post": post,
        "page_name": post_title_text,
        "comments": comments,
        'link': request.build_absolute_uri(post.get_absolute_url()),
    }
    return render(request, "blog/detail.html", context)

def blog_author(request, author):
    posts = Post.objects.filter(

        author__author_slug__contains=author

    ).order_by("-created_on")
    posts = render_blog_preview(posts)

    author_name = Author.objects.get(author_slug=author)

    context = {

        "author": author,
        "page_name": author_name,
        "posts": posts,

    }

    return render(request, "blog/author.html", context)

def index(request):
        video = get_latest_video_id("https://www.youtube.com/feeds/videos.xml?channel_id=UCEnLsvcq1eFkSFFAIqBDgUw")
        posts = tcv_posts("https://thecollegeview.ie/wp-json/wp/v2/posts?per_page=3&orderby=date&_fields=id,date,title,content,link,author,featured_media")
        awards = Award.objects.all()
        previous, current, next_show = get_date_time()

            
        return render(request, 'index.html', {'stats_data': index_stats_data,
                                              'subgroups_data': index_subgroups,
                                              'merch': merch,
            'row_1_display': "display: none;", 
                                            'row_2_display': "display: none;",
                                            'row_3_display': "display: none;",
                                          'page_name': 'Home', 
                                          'latest_video_id' : video, 
                                          'previous_show': previous, 
                                          'current_show': current, 
                                          'next_show': next_show,
                                            'event_status': "No events at the moment, check back later!",
                                            'awards': awards,
                                            'posts': posts,
                                            'homepage_carousel': homepage_carousel,
                                          })
        
def tcv(request):
    posts = tcv_posts("https://thecollegeview.ie/wp-json/wp/v2/posts?per_page=10&orderby=date&_fields=id,date,title,content,link,author,featured_media")
    news = tcv_posts("https://thecollegeview.ie/wp-json/wp/v2/posts?per_page=3&orderby=date&categories=4&_fields=id,date,title,content,link,author,featured_media")
    sport = tcv_posts("https://thecollegeview.ie/wp-json/wp/v2/posts?per_page=3&orderby=date&categories=7&_fields=id,date,title,content,link,author,featured_media")
    editors1 = CommitteeMember.objects.filter(position="Editor in Chief")
    editors2 = CommitteeMember.objects.filter(position="Webmaster")
    editors = editors1 | editors2
    return render(request, 'thecollegeview.html', {'page_name': 'The College View', 'posts': posts, 'news': news, 'sport': sport, 'family_tree' : tcv_family_tree, 'editors': editors})

def committee(request):
    committee_members = CommitteeMember.objects.all()
    committee_page_info = CommitteePage.objects.all().first()
    return render(request, 'committee.html', {'page_name': 'Committee', 'committee_members': committee_members, 'committee_page_info': committee_page_info})

def committee_history(request):
    committee_history = CommitteeHistory.objects.all()
    return render(request, 'committee_history.html', {'page_name': 'Committee History', 'committee_history': committee_history})

def contact(request):
    return render(request, 'contact.html', {'page_name': 'Contact'})

def dcutv(request):
    channel_url = "https://www.youtube.com/feeds/videos.xml?channel_id=UCEnLsvcq1eFkSFFAIqBDgUw"
    video = get_latest_video_id(channel_url)
    most_recent_videos = get_latest_video_ids(channel_url)
    tv_managers = CommitteeMember.objects.filter(position="TV Manager")
    return render(request, 'dcutv.html', {'page_name': 'DCUtv', 'tv_thursday' : 'RON9_ByY190', 'latest_video_id' : video, 'most_recent_videos': most_recent_videos, 'tv_managers': tv_managers, 'dcutv_carousel': dcutv_carousel, 'stats_data': dcutv_stats_data})

def gallery(request):
    gallery_page_info = GalleryPage.objects.all().first()
    image_urls = list_images()
    return render(request, 'gallery.html', {'page_name': 'Gallery', 'gallery_page_info': gallery_page_info, 'images': image_urls})

def links(request):
    sheet_url = "https://docs.google.com/spreadsheets/d/1FdtqA7a0sJcs24NIYWQnOOxrUiNLf1YvwUsWhZ1feLw/edit?usp=sharing"
    linktree = process_linktree_data(sheet_url)
    return render(request, 'links.html', {'page_name': 'Links', 'linktree': linktree})

def links_tv(request):
    sheet_url = "https://docs.google.com/spreadsheets/d/1VP371L8_fwkd1CUE-1L-j01mVwlZaCqcmAZKfGTvZaY/edit?usp=sharing"
    linktree = process_linktree_data(sheet_url)
    return render(request, 'links.html', {'page_name': 'DCUtv Links', 'linktree': linktree})

def links_fm(request):
    sheet_url = "https://docs.google.com/spreadsheets/d/1LnPc8wIwyFr09Wiko6myMCbq-9sTApt9URh-nqw2i0A/edit?usp=sharing"
    linktree = process_linktree_data(sheet_url)
    return render(request, 'links.html', {'page_name': 'DCUfm Links', 'linktree': linktree})

def links_tcv(request):
    sheet_url = "https://docs.google.com/spreadsheets/d/1ssVVGWg9nvUxxmLXQwC_-T2XWxuqGfYDSLp5T4S-e9I/edit?usp=sharing"
    linktree = process_linktree_data(sheet_url)
    return render(request, 'links.html', {'page_name': 'The College View Links', 'linktree': linktree})

def swapweek(request):
    return render(request, 'swapweek.html', {'page_name': 'Swap Week'})

def memes(request):
    return render(request, 'memes.html', {'page_name': 'Memes'})

def dcufm(request):
    previous, current, next_show = get_date_time()
    family_tree = DCUfmFamilyTree.objects.all()
    fm_managers = CommitteeMember.objects.filter(position="FM Manager")
    return render(request, 'dcufm.html', {'page_name': 'DCUfm', 'previous_show': previous, 'current_show': current, 'next_show': next_show, 'family_tree': family_tree, 'fm_managers': fm_managers, 'stats_data': dcufm_stats_data, 'subgroups_data': dcufm_subgroups})

def page_not_found(request):
    return render(request, '404.html', {'page_name': '404'})