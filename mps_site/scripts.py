from datetime import datetime
import feedparser
import yt_dlp as youtube_dl
import requests 
from bs4 import BeautifulSoup
import json
import pandas as pd

def tcv_posts(tcv_url):
    posts = []
    try:
        # Set a timeout for the request
        response = requests.get(tcv_url, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors
        posts = response.json()
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching posts: {e}")
        return posts

    for post in posts:
        try:
            soup = BeautifulSoup(post['content']['rendered'], 'html.parser')
            post['content_plain'] = soup.get_text()

            first_image = soup.find('img')
            post['first_image'] = first_image['src'] if first_image else None

            post['formatted_date'] = datetime.strptime(post['date'], '%Y-%m-%dT%H:%M:%S').strftime('%B %d, %Y')

            author_url = f"https://thecollegeview.ie/wp-json/wp/v2/users/{post['author']}"
            try:
                author_response = requests.get(author_url, timeout=10)
                author_response.raise_for_status()  # Raise an exception for HTTP errors
                author_data = author_response.json()
                post['author_name'] = author_data['name']
                post['author_slug'] = author_data['slug']
            except requests.exceptions.RequestException as e:
                print(f"An error occurred while fetching author data: {e}")
                post['author_name'] = None
                post['author_slug'] = None
        except Exception as e:
            print(f"An error occurred while processing post data: {e}")
            continue

    return posts

def process_linktree_data(sheet_url):
    url_1 = sheet_url.replace('/edit', '/export?format=csv&')
    texts = pd.read_csv(url_1, usecols= ['TEXT'])
    links = pd.read_csv(url_1, usecols= ['LINK'])
    text = [i[0] for i in texts.values]
    link = [i[0] for i in links.values]
    linktree = zip(text, link)
    return linktree

def get_date_time():
    date = datetime.now()
    day_of_week = date.weekday() + 1
    hour = date.hour

    messages = {
        1: {
            9: "Politics Nerdly", 
            10: "Out of the Woods", 
            11: "Limelight",
            12: "Is this it?",
            13: "Balikbayan Unbox",
            14: "The Football Show",
            15: "Paddock to Pitch",
            16: "Unqualified X Off Topic",
            17: "Shitty in the City",
            18: "Show X",
            19: "The Lunch Table",
        },
        2: {
            9: "The Dev Hour", 
            10: "Gossip Girls", 
            11: "Twang",
            12: "The Private Story",
            13: "Pop The Champagne",
            14: "Are you even listening to me?",
            15: "Ah here!",
            16: "Lawless Podcast",
            17: "Deep Dive",
            18: "Intrusive Intruders",
            19: "No shows on at the moment",
        
        },
        3: {
            9: "The Practice Podcast", 
            10: "The Dibs Boys", 
            11: "The Rendezvous",
            12: "My Next Guest with Sadhbh O'Grady", 
            13: "RuhRoh FM", 
            14: "Sound Waves",
            15: "Assia + Leah", 
            16: "We need therapy", 
            17: "4 Girls 1 Brain",
            18: "The Dining Table", 
            19: "Tipsey Tuesdays",
        },
        4: {
            9: "For the Plot", 
            10: "Neil Fitzgerald", 
            11: "Morning Debrief with Cian and Lauren",
            12: "Cinechat", 
            13: "Action Replay", 
            14: "Beating around the Bush",
            15: "The Shane O'Loughlin Podcast", 
            16: "The Killian Burke Podcast", 
            17: "It's a Groovement",
            18: "Windows Down", 
            19: "The Original Sin",
        },
        5: {
            9: "Fed Up Fridays", 
            10: "No shows on at the moment", 
            11: "The Lore",
            12: 'The "O" Show', 
            13: "HerVoice", 
            14: "Newswire",
            15: "Lights Camera Action", 
            16: "A Game of Two Halves", 
            17: "The Dugout",
            18: "No shows on at the moment", 
            19: "No shows on at the moment",
        },
    }

    if 1 <= day_of_week <= 5 and 9 <= hour < 19:
        previous_show = messages[day_of_week].get(hour - 1, "No shows on at the moment")
        current_show = messages[day_of_week].get(hour, "No shows on at the moment")
        next_show = messages[day_of_week].get(hour + 1, "No shows on at the moment")
    else:
        previous_show = current_show = next_show = "No shows on at the moment"

    return previous_show, current_show, next_show

"""def get_date_time_12_hour():
    date = datetime.datetime.now()
    hour = date.hour
    minute = date.minute
    weekday = date.weekday()

    messages = {
        9: "Intro & Interview",
        9.5: "The Smelly Show(nose plugs advised) X The UnOriginal Sin",
        10: "Guess Who DCU",
        10.5: "Is This It?",
        11: "Unqualified X OffTopic",
        11.5: "Carpool Karaoke FM Edition",
        12: "What Not To Do In Prague",
        12.5: "Sorting Out Your Lore",
        13: "Action Replay X The Dugout",
        13.5: "Newswire",
        14: "Soundwaves: Blind Ranking",
        14.5: "Sea Week",
        15: "The Practice Pod X For The Plot",
        15.5: "Shitty In The City",
        16: "Pop The Champagne",
        16.5: "Committea",
        17: "The Lunch Table",
        17.5: "Lawless Podcast",
        18: "TV V FM",
        18.5: "Deep Dive",
        19: "Balikbayan Unbox: Pinoy Henyo",
        19.5: "My Next Guest X Out Of The Woods X The Shane O'Loughlin Podcast",
        20: "DIBS Boys Broadcast Special",
        20.5: "Auction X Wax World"
    }
    if 9 <= hour < 21:
        if minute >= 30:
            hour += 0.5
        current_show = messages.get(hour, "No shows on at the moment")
        previous_show = messages.get(hour - 0.5, "No shows on at the moment")
        next_show = messages.get(hour + 0.5, "No shows on at the moment")
    else:
        previous_show = current_show = next_show = "No shows on at the moment"

    return previous_show, current_show, next_show"""

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
    
def get_donation_count_fm():
    URL = "https://www.idonate.ie/fundraiser/MediaProductionSociety11"
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0"} 
    r = requests.get(url=URL, headers=headers) 
    soup = BeautifulSoup(r.content, 'html5lib')
    current_donation = soup.find('div', attrs = {'class':'ifs-right-fundraisers-head'}) 
    donation_target = soup.find('div', attrs = {'class':'support-cause'}) 
    current_donation_amount = int(str(current_donation).split()[3].split("€")[1].split("<")[0].replace(",",""))
    goal_amount = int(str(donation_target).split("€")[1].split("<")[0].replace(",",""))
    return current_donation_amount, goal_amount

def get_event_data():
  data = {}
  events = {}
  URL = f"https://dcuclubsandsocs.ie/society/media-production"
  headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0"} 
  r = requests.get(url=URL, headers=headers) 
  soup = BeautifulSoup(r.content, 'html5lib')
  events_data = soup.find('div', attrs = {'id':'events'})
  try:
    event_count = int(events_data.find('span', attrs = {'class':'float-right badge badge-light'}).text)
  except:
    event_count = 0
  if event_count == 0:
    data['event_count'] = event_count
    data['events'] = None
    return data
  event_table = events_data.find('div', attrs = {'class':'table-responsive'})
  events_info_list = event_table.find_all('tr', attrs={'class':'show_info pointer'})
  events_info_hidden = event_table.find_all('tr', attrs={'class':'d-none'})

  for i in range(0, len(events_info_list) - 1, 2):
    event_info = events_info_list[i]
    try:
      event_image = event_info.find('img')['src']
    except:
      event_image = "static/assets/img/other/upcoming_event.png"
    event_name = event_info.find('th', attrs={'class': 'h5 align-middle'}).text.strip()
    events["event_" + str(i // 2)] = {'name': event_name, 'image': event_image}

  for i in range(1, len(events_info_list), 2):
    event_info = events_info_list[i]
    event_data = event_info.find_all('td', attrs={'class': 'text-center align-middle'})
    events["event_" + str(i // 2)]['start'] = event_data[1].find('b').text
    events["event_" + str(i // 2)]['end'] = event_data[2].find('b').text
    events["event_" + str(i // 2)]['cost'] = event_data[3].find('b').text
    events["event_" + str(i // 2)]['capacity'] = event_data[4].find('b').text
    events["event_" + str(i // 2)]['type'] = event_data[5].find('b').text
    events["event_" + str(i // 2)]['location'] = events_info_hidden[i].find('b').text
    events["event_" + str(i // 2)]['description'] = events_info_hidden[i].find('p')
    
  data['event_count'] = event_count
  data['events'] = events                                                                                           
  return data
  
  

FOLDER_ID = ''
API_KEY = ''

def list_images():
    url = f'https://www.googleapis.com/drive/v3/files?q="{FOLDER_ID}" in parents&key={API_KEY}'
    response = requests.get(url)
    data = response.json()
    
    image_urls = []
    if 'files' in data:
        for item in data['files']:
            file_id = item['id']
            file_name = item['name']
            file_url = f'https://drive.usercontent.google.com/download?id={file_id}'
            image_urls.append({'name': file_name, 'url': file_url})
            
    return image_urls