from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import *
from .scripts import *
import json
from django.utils.safestring import mark_safe
from datetime import datetime
import markdown
from .utils import *
from .data.homepage import *
from .data.dcufm import *
from .data.dcutv import *
from .data.thecollegeview import *
from .data.committee import *
from .data.loans import *
from concurrent.futures import ThreadPoolExecutor, as_completed

def ordinal(n):
    if 10 <= n % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return f"{n}{suffix}"

def format_event_date(date_str):
    date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
    day = ordinal(date_obj.day)
    return date_obj.strftime(f"%a {day} %b at %H:%M")

def index(request):
        video = get_latest_video_id("https://www.youtube.com/feeds/videos.xml?channel_id=UCEnLsvcq1eFkSFFAIqBDgUw")
        posts = tcv_posts("https://thecollegeview.ie/wp-json/wp/v2/posts?per_page=3&orderby=date&_fields=id,date,title,content,link,author,featured_media")
        previous, current, next_show = get_date_time()
        events = requests.get("https://clubsandsocs.jakefarrell.ie/dcuclubsandsocs.ie/society/media-production/events").json()
        donation_data = get_donation_count()
        current_donation_amount = donation_data["totalRaised"]
        goal_amount = donation_data["targetAmount"]

        for event in events:
            event['formatted_start'] = format_event_date(event['start'])
            event['formatted_end'] = format_event_date(event['end'])

        return render(request, 'index.html', 
                       {'stats_data': homepage_stats_data,
                        'subgroups_data': homepage_subgroups,
                        'merch': homepage_merch,
                        'events': events,
                        'page_name': 'Home', 
                        'latest_video_id' : video, 
                        'previous_show': previous, 
                        'current_show': current, 
                        'next_show': next_show,
                        'homepage_awards': homepage_awards,
                        'posts': posts,
                        'homepage_carousel': homepage_carousel,
                        'current_donation_amount': current_donation_amount,
                        'goal_amount': goal_amount})
        
def tcv(request):
    categories = {
        'posts': construct_tcv_url(per_page=10),
        'news': construct_tcv_url(category=4),
        'sport': construct_tcv_url(category=7),
        'feat': construct_tcv_url(category=5),
        'opinion': construct_tcv_url(category=687),
        'lifestyle': construct_tcv_url(category=220),
        'satire': construct_tcv_url(category=9890),
        'hype': construct_tcv_url(category=6),
        'irish': construct_tcv_url(category=68),
    }

    with ThreadPoolExecutor() as executor:
        future_to_category = {executor.submit(tcv_posts, url): category for category, url in categories.items()}
        results = {category: future.result() for future, category in future_to_category.items()}

    editors = [member for member in committee_list["members"] if member["position"] in ["Editor in-Chief", "Deputy Editor in-Chief"]]

    return render(request, 'thecollegeview.html', {
        'page_name': 'The College View',
        **results,
        'family_tree': tcv_family_tree,
        'editors': editors
    })
    
def ads(request):
    return render(request, 'ads.html', {'page_name': 'Ad Package Randomiser'})

def committee(request):
    committee_members = CommitteeMember.objects.all()
    return render(request, 'committee.html', 
                  {'page_name': 'Committee', 
                   'committee_members': committee_members,
                   'committee_list': committee_list,
                   'committee_video_id': '1wiscXP9nw0'})

def committee_history(request):
    committee_history = CommitteeHistory.objects.all()
    return render(request, 'committee_history.html', 
                  {'page_name': 'Committee History', 
                   'committee_history': committee_history})

def committee_history_detail(request, year):
    committee_history = CommitteeHistory.objects.get(year=year)
    return render(request, 'committee_history_detail.html', 
                  {'page_name': committee_history.title, 
                   'committee_history': committee_history})

def contact(request):
    return render(request, 'contact.html', 
                  {'page_name': 'Contact'})

def dcutv(request):
    tv_managers = [member for member in committee_list["members"] if member["position"] == "TV Manager"]
    donation_data = get_donation_count()
    current_donation_amount = donation_data["totalRaised"]
    goal_amount = donation_data["targetAmount"]
    return render(request, 'dcutv.html', 
                  {'page_name': 'DCUtv', 
                   'tv_thursday' : 'RON9_ByY190', 
                   'latest_video_id' : get_latest_video_id("https://www.youtube.com/feeds/videos.xml?channel_id=UCEnLsvcq1eFkSFFAIqBDgUw"), 
                   'most_recent_videos': get_latest_video_ids("https://www.youtube.com/feeds/videos.xml?channel_id=UCEnLsvcq1eFkSFFAIqBDgUw"), 
                   'tv_managers': tv_managers,
                   'dcutv_carousel': dcutv_carousel, 
                   'stats_data': dcutv_stats_data,
                   'committee_video_id': '1wiscXP9nw0',
                   'current_donation_amount': current_donation_amount,
                   'goal_amount': goal_amount})
    
def thedev(request):
    managers = [member for member in committee_list["members"] if member["position"] == "Brand Design Officer"]
    categories = {
        'thedev': construct_tcv_url(category=10473),
    }

    with ThreadPoolExecutor() as executor:
        future_to_category = {executor.submit(tcv_posts, url): category for category, url in categories.items()}
        results = {category: future.result() for future, category in future_to_category.items()}
        
    return render(request, 'thedev.html', {'page_name': 'The Dev',
                                           'managers': managers,
                                           **results})

def gallery(request):
    gallery_page_info = GalleryPage.objects.all().first()
    return render(request, 'gallery.html', {'page_name': 'Gallery', 'gallery_page_info': gallery_page_info})

def loans(request):
    return render(request, 'loans.html', {'page_name': 'DCUtv Loans', 'loans_data': loans_data})

def dcufm(request):
    previous, current, next_show = get_date_time()
    family_tree = DCUfmFamilyTree.objects.all()
    fm_managers = [member for member in committee_list["members"] if member["position"] == "FM Manager"]
    return render(request, 'dcufm.html', 
                  {'page_name': 'DCUfm', 
                   'previous_show': previous, 
                   'current_show': current, 
                   'next_show': next_show, 
                   'family_tree': family_tree, 
                   'fm_managers': fm_managers, 
                   'stats_data': dcufm_stats_data, 
                   'subgroups_data': dcufm_subgroups,
                   'shows_data': dcufm_shows,
                   'dcufm_carousel': dcufm_carousel,
                   'dcufm_subcommittee': dcufm_subcommittee})

def page_not_found(request):
    return render(request, '404.html', {'page_name': '404'})

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

def links_dev(request):
    sheet_url = "https://docs.google.com/spreadsheets/d/1DhR09FjdZL2sNkYrPAm18dZOL6hhmmGtBrwbWWD0swQ/edit?usp=sharing"
    linktree = process_linktree_data(sheet_url)
    return render(request, 'links.html', {'page_name': 'The Dev Links', 'linktree': linktree})

def swapweek(request):
    return render(request, 'swapweek.html', {'page_name': 'Swap Week'})

def memes(request):
    return render(request, 'memes.html', {'page_name': 'Memes'})





# BLOG STUFF

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