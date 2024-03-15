from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .fm_time import get_date_time
from .event_data import get_event_data
from .latest_video import get_latest_video_id
from .main_single import get_donation_count_fm
import json
import pandas as pd
from django.utils.safestring import mark_safe

def index(request):
        channel_url = "https://www.youtube.com/feeds/videos.xml?channel_id=UCEnLsvcq1eFkSFFAIqBDgUw"
        video = get_latest_video_id(channel_url)
        awards = Award.objects.all()
        previous, current, next_show = get_date_time()
        get_event_data()
        about = About.objects.all().first()
        with open('mps_site/event-data.json', 'r') as file:
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
                                          })

def committee(request):
    return render(request, 'committee.html', {'page_name': 'Committee'})

def contact(request):
    return render(request, 'contact.html', {'page_name': 'Contact'})

def dcutv(request):
    channel_url = "https://www.youtube.com/feeds/videos.xml?channel_id=UCEnLsvcq1eFkSFFAIqBDgUw"
    video = get_latest_video_id(channel_url)
    return render(request, 'dcutv.html', {'page_name': 'DCUtv', 'tv_thursday' : 'RON9_ByY190', 'latest_video_id' : video})

def gallery(request):
    return render(request, 'gallery.html', {'page_name': 'Gallery'})

"""def blog(request):
    return render(request, 'blog.html', {'page_name': 'Blog'})

def merch(request):
    return render(request, 'merch.html', {'page_name': 'Merch'})"""

def links(request):
    sheet_url = "https://docs.google.com/spreadsheets/d/1FdtqA7a0sJcs24NIYWQnOOxrUiNLf1YvwUsWhZ1feLw/edit?usp=sharing"
    url_1 = sheet_url.replace('/edit', '/export?format=csv&')
    texts = pd.read_csv(url_1, usecols= ['TEXT'])
    links = pd.read_csv(url_1, usecols= ['LINK'])
    text = [i[0] for i in texts.values]
    link = [i[0] for i in links.values]
    linktree = zip(text, link)
    context = {
        'linktree': linktree,
    }
    return render(request, 'links.html', {'page_name': 'Links', 'linktree': linktree})

def links_tv(request):
    sheet_url = "https://docs.google.com/spreadsheets/d/1VP371L8_fwkd1CUE-1L-j01mVwlZaCqcmAZKfGTvZaY/edit?usp=sharing"
    url_1 = sheet_url.replace('/edit', '/export?format=csv&')
    texts = pd.read_csv(url_1, usecols= ['TEXT'])
    links = pd.read_csv(url_1, usecols= ['LINK'])
    text = [i[0] for i in texts.values]
    link = [i[0] for i in links.values]
    linktree = zip(text, link)
    context = {
        'linktree': linktree,
    }
    return render(request, 'links.html', {'page_name': 'DCUtv Links', 'linktree': linktree})

def links_fm(request):
    sheet_url = "https://docs.google.com/spreadsheets/d/1LnPc8wIwyFr09Wiko6myMCbq-9sTApt9URh-nqw2i0A/edit?usp=sharing"
    url_1 = sheet_url.replace('/edit', '/export?format=csv&')
    texts = pd.read_csv(url_1, usecols= ['TEXT'])
    links = pd.read_csv(url_1, usecols= ['LINK'])
    text = [i[0] for i in texts.values]
    link = [i[0] for i in links.values]
    linktree = zip(text, link)
    context = {
        'linktree': linktree,
    }
    return render(request, 'links.html', {'page_name': 'DCUfm Links', 'linktree': linktree})

def links_tcv(request):
    sheet_url = "https://docs.google.com/spreadsheets/d/1ssVVGWg9nvUxxmLXQwC_-T2XWxuqGfYDSLp5T4S-e9I/edit?usp=sharing"
    url_1 = sheet_url.replace('/edit', '/export?format=csv&')
    texts = pd.read_csv(url_1, usecols= ['TEXT'])
    links = pd.read_csv(url_1, usecols= ['LINK'])
    text = [i[0] for i in texts.values]
    link = [i[0] for i in links.values]
    linktree = zip(text, link)
    context = {
        'linktree': linktree,
    }
    return render(request, 'links.html', {'page_name': 'The College View Links', 'linktree': linktree})

"""def comingsoon(request):
    return render(request, 'comingsoon.html', {'page_name': 'Coming Soon'})"""

def swapweek(request):
    return render(request, 'swapweek.html', {'page_name': 'Swap Week'})

def memes(request):
    return render(request, 'memes.html', {'page_name': 'Memes'})

def dcufm(request):
    previous, current, next_show = get_date_time()
    get_donation_count_fm()
    family_tree = DCUfmFamilyTree.objects.all()
    return render(request, 'dcufm.html', {'page_name': 'DCUfm', 'previous_show': previous, 'current_show': current, 'next_show': next_show, 'family_tree': family_tree})


def donate(request):
    return redirect('https://www.idonate.ie/fundraiser/MediaProductionSociety11')

def broadcast(request):
    return redirect('https://youtube.com/dcumps')

def lounge(request):
    return redirect('https://lounge.live/lounges/kr53i9b6')

def join(request):
    return redirect('https://dcuclubsandsocs.ie/society/media-production')

def thinktank(request):
    return redirect('https://chat.whatsapp.com/EBupVbTpWX01uJvBp5r24D')

def tcv(request):
    return redirect('https://www.thecollegeview.ie/')

def youtube(request):
    return redirect('https://youtube.com/dcumps')

def tiktok(request):
    return redirect('https://www.tiktok.com/@dcumps')

def instagram(request):
    return redirect('https://instagram.com/dcumps')

def facebook(request):
    return redirect('https://facebook.com/dcumps')

def twitter(request):
    return redirect('https://twitter.com/dcumps')

def twitch(request):
    return redirect('https://twitch.tv/dcufm')
