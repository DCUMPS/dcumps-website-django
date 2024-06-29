from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import *
from .scripts import *
import json
from django.utils.safestring import mark_safe
from datetime import datetime

def blog_index(request):
    posts = Post.objects.all().order_by("-created_on")
    context = {
        "posts": posts,
        "page_name": "Blog"
    }

    return render(request, "blog/index.html", context)

def blog_category(request, category):

    posts = Post.objects.filter(

        categories__name__contains=category

    ).order_by("-created_on")

    context = {

        "category": category,
        "page_name": category,
        "posts": posts,

    }

    return render(request, "blog/category.html", context)

# blog/views.py

# ...

def blog_detail(request, slug):
    post = get_object_or_404(Post, post_slug=slug)
    comments = Comment.objects.filter(post=post)
    context = {
        "post": post,
        "page_name": post.title,
        "comments": comments,
        'link': request.build_absolute_uri(post.get_absolute_url()),
    }
    return render(request, "blog/detail.html", context)

def blog_author(request, author):
    posts = Post.objects.filter(

        author__author_slug__contains=author

    ).order_by("-created_on")

    context = {

        "author": author,
        "page_name": posts,
        "posts": posts,

    }

    return render(request, "blog/author.html", context)

def index(request):
        channel_url = "https://www.youtube.com/feeds/videos.xml?channel_id=UCEnLsvcq1eFkSFFAIqBDgUw"
        tcv_url = "https://thecollegeview.ie/wp-json/wp/v2/posts?per_page=3&orderby=date"
        response = requests.get(tcv_url)
        posts = response.json()
        for post in posts:
            soup = BeautifulSoup(post['content']['rendered'], 'html.parser')
            post['content_plain'] = soup.get_text()

            first_image = soup.find('img')
            post['first_image'] = first_image['src'] if first_image else None

            post['formatted_date'] = datetime.strptime(post['date'], '%Y-%m-%dT%H:%M:%S').strftime('%B %d, %Y')

            author_url = f"https://thecollegeview.ie/wp-json/wp/v2/users/{post['author']}"
            author_response = requests.get(author_url)
            author_data = author_response.json()
            post['author_name'] = author_data['name']
            post['author_slug'] = author_data['slug']

        video = get_latest_video_id(channel_url)
        awards = Award.objects.all()
        previous, current, next_show = get_date_time()
        get_event_data()
        donation_amount, donation_goal = get_donation_count_fm()
        about = About.objects.all().first()
        with open('mps_site/static/event-data.json', 'r') as file:
            data = json.load(file)
            event_count = data['event_count']
            event_1_name = ""
            event_1_start = ""
            event_1_end = ""
            event_1_location = ""
            event_1_description = ""
            event_2_name = ""
            event_2_start = ""
            event_2_end = ""
            event_2_location = ""
            event_2_description = ""
            event_3_name = ""
            event_3_start = ""
            event_3_end = ""
            event_3_location = ""
            event_3_description = ""
            event_status = ""
            event_1_image = ""
            event_2_image = ""
            event_3_image = ""
            if event_count == 0:
                row_1_display = "display: none;"
                row_2_display = "display: none;"
                row_3_display = "display: none;"
                event_status = "No events at the moment, check back later!"
            if event_count >= 1:
                row_1_display = ""
                row_2_display = "display: none;"
                row_3_display = "display: none;"
                event_1_name = data['event_1_name']
                event_1_start = data['event_1_start']
                event_1_end = data['event_1_end']
                event_1_location = data['event_1_location']
                event_1_description = data['event_1_description']
                event_1_image = data['event_1_image']
            if event_count >= 2:
                row_1_display = ""
                row_2_display = ""
                row_3_display = "display: none;"
                event_2_name = data['event_2_name']
                event_2_start = data['event_2_start']
                event_2_end = data['event_2_end']
                event_2_location = data['event_2_location']
                event_2_description = data['event_2_description']
                event_2_image = data['event_2_image']
            if event_count >= 3:
                row_1_display = ""
                row_2_display = ""
                row_3_display = ""
                event_3_name = data['event_3_name']
                event_3_start = data['event_3_start']
                event_3_end = data['event_3_end']
                event_3_location = data['event_3_location']
                event_3_description = data['event_3_description']
                event_3_image = data['event_3_image']

            
        return render(request, 'index.html', {'row_1_display': row_1_display, 
                                            'row_2_display': row_2_display,
                                            'row_3_display': row_3_display,
                                          'page_name': 'Home', 
                                          'latest_video_id' : video, 
                                          'previous_show': previous, 
                                          'current_show': current, 
                                          'next_show': next_show,
                                          'event_count': event_count,
                                          'event_1_name': event_1_name,
                                          'event_1_start': event_1_start,
                                          'event_1_end': event_1_end,
                                          'event_1_location': event_1_location,
                                          'event_1_description': mark_safe(event_1_description),
                                          'event_2_name': event_2_name,
                                            'event_2_start': event_2_start,
                                            'event_2_end': event_2_end,
                                            'event_2_location': event_2_location,
                                            'event_2_description': mark_safe(event_2_description),
                                            'event_3_name': event_3_name,
                                            'event_3_start': event_3_start,
                                            'event_3_end': event_3_end,
                                            'event_3_location': event_3_location,
                                            'event_3_description': mark_safe(event_3_description),
                                            'event_status': event_status,
                                            'event_1_image': event_1_image,
                                            'event_2_image': event_2_image,
                                            'event_3_image': event_3_image,
                                            'awards': awards,
                                            'about': about,
                                            'donation_amount': donation_amount,
                                            'donation_goal': donation_goal,
                                            'posts': posts
                                          })

def committee(request):
    committee_members = CommitteeMember.objects.all()
    committee_page_info = CommitteePage.objects.all().first()
    return render(request, 'committee.html', {'page_name': 'Committee', 'committee_members': committee_members, 'committee_page_info': committee_page_info})

def contact(request):
    return render(request, 'contact.html', {'page_name': 'Contact'})

def dcutv(request):
    channel_url = "https://www.youtube.com/feeds/videos.xml?channel_id=UCEnLsvcq1eFkSFFAIqBDgUw"
    video = get_latest_video_id(channel_url)
    most_recent_videos = get_latest_video_ids(channel_url)
    return render(request, 'dcutv.html', {'page_name': 'DCUtv', 'tv_thursday' : 'RON9_ByY190', 'latest_video_id' : video, 'most_recent_videos': most_recent_videos})

def gallery(request):
    gallery_page_info = GalleryPage.objects.all().first()
    return render(request, 'gallery.html', {'page_name': 'Gallery', 'gallery_page_info': gallery_page_info})

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
    donation_amount, donation_goal = get_donation_count_fm()
    family_tree = DCUfmFamilyTree.objects.all()
    return render(request, 'dcufm.html', {'page_name': 'DCUfm', 'previous_show': previous, 'current_show': current, 'next_show': next_show, 'family_tree': family_tree, 'donation_amount': donation_amount, 'donation_goal': donation_goal})

"""def comingsoon(request):
    return render(request, 'comingsoon.html', {'page_name': 'Coming Soon'})"""

def blog(request):
    return render(request, 'blog.html', {'page_name': 'Blog'})

"""def merch(request):
    return render(request, 'merch.html', {'page_name': 'Merch'})"""

def page_not_found(request):
    return render(request, '404.html', {'page_name': '404'})