from datetime import datetime
import feedparser
import yt_dlp as youtube_dl
import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
import re


def construct_tcv_url(per_page=3, category=None):
    base_url = "https://thecollegeview.ie/wp-json/wp/v2/posts"
    query_params = f"?per_page={per_page}&orderby=date&_fields=id,date,title,content,link,author,featured_media"
    if category:
        query_params += f"&categories={category}"
    return base_url + query_params


def fetch_data(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None


def get_featured_media(media_id):
    media_data = fetch_data(
        f"https://thecollegeview.ie/wp-json/wp/v2/media/{media_id}")
    return media_data['guid']['rendered'] if media_data else None


def tcv_posts(url):
    posts = fetch_data(url)
    if not posts:
        return []

    for post in posts:
        soup = BeautifulSoup(post['content']['rendered'], 'html.parser')
        post['content_plain'] = soup.get_text()
        first_image = soup.find('img')
        post['first_image'] = first_image['src'] if first_image else get_featured_media(
            post['featured_media'])

        post['formatted_date'] = datetime.strptime(
            post['date'], '%Y-%m-%dT%H:%M:%S').strftime('%B %d, %Y')

        author_data = fetch_data(
            f"https://thecollegeview.ie/wp-json/wp/v2/users/{post['author']}")
        if author_data:
            post['author_name'] = author_data.get('name')
            post['author_slug'] = author_data.get('slug')
        else:
            post['author_name'] = post['author_slug'] = None

    return posts


def process_linktree_data(sheet_url):
    url_1 = sheet_url.replace('/edit', '/export?format=csv&')
    texts = pd.read_csv(url_1, usecols=['TEXT'])
    links = pd.read_csv(url_1, usecols=['LINK'])
    text = [i[0] for i in texts.values]
    link = [i[0] for i in links.values]
    linktree = zip(text, link)
    return linktree


from datetime import datetime

def get_date_time():
    date = datetime.now()
    day_name = date.strftime("%A")
    hour = date.hour

    timetable = {
        "Monday": {
            9: "The Football Show: Dylan Clarkin, Robert Curran",
            10: "Action Replay: Eoin O'Sullivan, Mya Breen",
            11: "No shows on at the moment",
            12: "Fresh Princes on Air: Jake Dalton, Paul Farrell, Beth o Connor, Shaney McConnon",
            13: "OnlySports: Oisin O Brien and Ryan Mulvaney",
            14: "Gossip Girls: Zöe Percival, Erin Miller, Mia Mulvaney, Kacey Matthews",
            15: "This & Yap: Olivia Doyle & Mya Breen",
            16: "CrowTalk: Sam Kennedy, Rory Dalton, David Keyes, Rian Lowry",
            17: "The Theme Machine!: Daire Canny",
            18: "Crucial Media for a Internet Generation: Daniel Salmon",
        },
        "Tuesday": {
            9: "The Dibs Boys: Matthew Willis, Finn McElwain, Luke Nolan",
            10: "Track Talk: Sabina Donnery, Paddy Wanna, Emma Montalbani",
            11: "Impreviews: Shane Codd",
            12: "Alex, Dylan and Ruby on DCUFM: Alex Rowley, Dylan Hand, Ruby McManus",
            13: "Send Help: Erin Reel, Saoirse MacCarthy",
            14: "CineChat: Torna Mulconry",
            15: "Tipsy Tuesdays: Jack Reynolds, Ronan Casey",
            16: "Newswire: Daniel Hayden, Grace Collins",
            17: "Perfecting Perfection: Aoibhín McEvoy and Dearbhla McCormack",
            18: "Screen Queens: Roisin McManus, Beatriz Antunes, Sophie Finn, Zuzana Palenikova",
        },
        "Wednesday": {
            9: "Evan’s Double Entendre: Evan Dalton",
            10: "Show Ate: Kaitlyn Firmo",
            11: "Scene-It!: Iara Moreira, Aria Kazi",
            12: "The Grandstand Sports Show: Tiarnán O’Kelly and Evan Dalton",
            13: "Ah Here!: Alyson Stewart, Ava Shannon, Ellen McCahil, Ella Verveen and Georgia Ryan",
            14: "Fly on the wall: Katie Walsh, Holly Smith",
            15: "DCYouWantTheNews: Aaron Casey and Ailish Connor",
            16: "Five Stars from Comms: Lauren Joyce, Shona Kiely, Eanna Kavanagh, Sophie Egan, Eabha Kelly",
            17: "Is this it?: Helen Jenkins, Darragh Hallissy, Jack Dempsey, Max Daly, Daniel O’ Shea",
            18: "No shows on at the moment",
        },
        "Thursday": {
            9: "Serial Thrillas: Sam Cummins agus Eoghan Murphy",
            10: "The Morning Debrief: Aoife Loughrey, Katie Keating, Ella Geary",
            11: "The Original Sin: Sam Murray - Douglas Murray",
            12: "Journalism Away Days: Patrick Walsh, Adam Balmer, Liam Rigley",
            13: "The Dugout: Eoin O'Sullivan, Rian Lowry, Cian Mulligan, James Whittaker",
            14: "The Lore: Molly McGurrin, Allyson Lambe, Shelby Brennan, Jane O’Reilly",
            15: "Show Y: Alex Lyons, Jack Mc Avinue",
            16: "Limelight: Lauren Joyce, Holly O'Neill",
            17: "Her Voice: Lauren Joyce",
            18: "Wellness Check with VP for Wellbeing: Jamie Mangan",
        },
        "Friday": {
            9: "Diabhal scéal: Siobhra Behan, Carla Reilly, Kate Rayel",
            10: "Sound Check: Lauren textor, Adam Van ekereen, Katie monks",
            11: "Subway Wednesdays: Sean Baker, Aaron Conway",
            12: "For The Plot: Leonor Selas Amaral, Lily Quinn & Shane Meleady",
            13: "Soundwaves: Sarah Duff, Sophie King",
            14: "ChitChatFM: Emily Mullally, Clodagh Mahon, Ciara Stell",
            15: "Ode to Youth: Debby Ugoiwa",
            16: "No shows on at the moment",
            17: "No shows on at the moment",
            18: "No shows on at the moment",
        }
    }

    if day_name in timetable and 9 <= hour <= 18:
        current_show = timetable[day_name].get(hour, "No shows on at the moment")
        previous_show = timetable[day_name].get(hour - 1, "No shows on at the moment")
        next_show = timetable[day_name].get(hour + 1, "No shows on at the moment")
    else:
        current_show = previous_show = next_show = "No shows on at the moment"

    return previous_show, current_show, next_show



def get_latest_video_id(channel_url):
    feed = feedparser.parse(channel_url)

    if len(feed.entries) > 0:
        latest_video_url = feed.entries[0].link
        video_id = latest_video_url.split('=')[-1]
        return video_id
    else:
        return None


def get_latest_video_ids(channel_url):
    feed = feedparser.parse(channel_url)
    video_ids = []

    for entry in feed.entries[:9]:
        video_url = entry.link
        video_id = video_url.split('=')[-1]
        video_ids.append(video_id)

    return video_ids


def get_most_popular_video_ids(channel_url, n=9):
    ydl_opts = {
        'quiet': True,
        'force_generic_extractor': True,
        'skip_download': True,
        'extract_flat': True,
        'match_filter': youtube_dl.utils.match_filter_func('view_count>=1000000'),
        'playlistend': n,
        'sort': 'view_count'
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(channel_url, download=False)
        video_ids = [entry['id'] for entry in info['entries']]
        return video_ids


def get_donation_count():
    URL = "https://www.idonate.ie/fundraiser/MediaProductionSociety12"
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0"}

    data = {
        'totalRaised': 0,
        'targetAmount': 0
    }

    try:
        r = requests.get(url=URL, headers=headers, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.content, 'html5lib')

        script_tag = soup.find('script', string=re.compile('totalRaised'))

        js_content = script_tag.string if script_tag else ''

        total_raised_match = js_content.replace('\\', '').split(',')

        for item in total_raised_match:
            if '"totalRaised":' in item:
                data['totalRaised'] = int(
                    float(item.split(':')[1].replace('"', '')))
            if '"targetAmount":' in item:
                data['targetAmount'] = int(
                    float(item.split(':')[1].replace('"', '')))

        return data

    except (requests.RequestException, ValueError, IndexError, AttributeError) as e:
        return data


def get_live_broadcast_shows():
    date = datetime.now()
    day_name = date.strftime("%A")
    current_time = date.strftime("%H:%M")
    current_hour = date.hour
    current_minute = date.minute

    timetable = {
        "Wednesday": {
            "20:00": "Broadcast Introduction",
            "20:30": "Lip Sync Battle",
            "21:00": "The Oscars",
            "21:30": "Focus Interview",
            "22:00": "Hot Wans",
            "22:30": "Sa(m)tas Corner",
            "23:00": "DCeUrovision",
            "23:30": "Freshers on Air",
        },
        "Friday": {
            "00:00": "Storytime with Holly",
            "00:20": "Doghouse",
            "00:40": "Inkmaster",
            "01:00": "Crowtalk",
            "01:30": "CommiTEA",
            "02:00": "Game Changer",
            "02:20": "Undercover boss",
            "02:40": "Weird Films & Queer Men in music",
            "03:00": "Bird Brains III: Bait Masters",
            "03:30": "Carpool Kareoke",
            "04:00": "Sexy Calendar",
            "04:30": "The Lore",
            "05:00": "Competitive Yapping",
            "05:20": "What did they just say?",
            "05:40": "The Wheel",
            "06:00": "The Thing is...",
            "06:30": "Are you smarter than a Comms Student?",
            "07:00": "Infuriating Guessing Game",
            "07:30": "Committee Bake off",
            "08:00": "Get Flexy!",
            "08:30": "The Voice DCU",
            "09:00": "This & Yap",
            "09:30": "Family Feud",
            "10:00": "Unlikely Things to Hear / Would I lie to you?",
            "10:30": "Spill your Guts or Fill your Guts",
            "11:00": "Battle of the FM Flagships",
            "11:30": "The DIBS Boys",
            "12:00": "Drama",
            "12:30": "Comms Dine with me",
            "13:00": "Her Campus",
            "13:30": "DCUtv Guesses",
            "14:00": "Action Replay vs The Dugout",
            "14:30": "Taskmaster",
            "15:00": "Price is Right: Londis Edition",
            "15:30": "Expectations Vs Reality",
            "16:00": "Franks Butcher Shop",
            "16:30": "Breaking News",
            "17:00": "DCU Seagulls",
            "17:30": "Six One",
            "18:00": "Lip Sync Battle 2",
            "18:30": "GoldenCards",
            "19:00": "Early Early Product Placement",
            "19:30": "Thursday Night Live",
            "20:00": "Farewells",
        }
    }

    if day_name in timetable:
        sorted_times = sorted(timetable[day_name].keys())

        current_show_b = "No shows on at the moment"
        previous_show_b = "No shows on at the moment"
        next_show_b = "No shows on at the moment"

        for i, show_time in enumerate(sorted_times):
            if current_time >= show_time:
                current_show_b = timetable[day_name][show_time]
                if i > 0:
                    previous_show_b = timetable[day_name][sorted_times[i - 1]]
                if i + 1 < len(sorted_times):
                    next_show_b = timetable[day_name][sorted_times[i + 1]]
                break
    else:
        current_show_b = previous_show_b = next_show_b = "No shows on at the moment"

    return previous_show_b, current_show_b, next_show_b
