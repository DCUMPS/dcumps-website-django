from datetime import datetime
import feedparser
import yt_dlp as youtube_dl
import requests 
from bs4 import BeautifulSoup
import json
import pandas as pd

def tcv_posts(tcv_url):
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

  URL = "https://dcuclubsandsocs.ie/society/media-production"
  headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0"} 
  r = requests.get(url=URL, headers=headers) 
  soup = BeautifulSoup(r.content, 'html5lib')


  image_test = soup.find_all('img', attrs = {'class' : 'img-thumbnail'})
  src_list = [img['src'] for img in image_test]

  test = soup.find('div', attrs = {'id':'events_table'}) 
  event_count = soup.find('span', attrs = {'class':'float-right badge badge-light'})
  event_count = int(event_count.text)

  try:
    description = test.find_all('b')
  except AttributeError:
    event_count = 0
  try:
    name = test.find_all('th')
  except AttributeError:
    event_count = 0

  starts = []

  starts_row = soup.find_all('td', text='Starts')
  for item in starts_row:
    starts_time = item.find_next('td').get_text(strip=True)
    starts.append(starts_time)

  ends = []

  ends_row = soup.find_all('td', text='Ends')
  for item in ends_row:
    ends_time = item.find_next('td').get_text(strip=True)
    ends.append(ends_time)

  h5_tags = soup.find_all('h5')
  locations = [tag.find('b').text.strip() for tag in h5_tags if 'Location:' in tag.text]

  td_tags = soup.find_all('td', class_='break-all')
  descriptions = []
  for tag in td_tags:
    hr_tag = tag.find('hr')
    content_after_hr = hr_tag.find_next_siblings()
    text_after_hr = [tag.get_text(strip=True) for tag in content_after_hr]
    descriptions.append("<br>".join(text_after_hr))


  data = {}

  data['event_count'] = event_count

  if event_count >= 1:
    data['event_1_name'] = name[0].text.strip()
    if len(src_list) > 1:
      data['event_1_image'] = src_list[1].strip()
    else:
      data['event_1_image'] = "static/assets/img/other/upcoming_event.png"
      
    data['event_1_start'] = starts[0]
    data['event_1_end'] = ends[0]
    data['event_1_location'] = locations[0]
    data['event_1_description'] = descriptions[0]

  if event_count >= 2:
    data['event_2_name'] = name[1].text.strip()
    if len(src_list) > 2:
      data['event_2_image'] = src_list[2].strip()
    else:
      data['event_2_image'] = "static/assets/img/other/upcoming_event.png"

    data['event_2_start'] = starts[1]
    data['event_2_end'] = ends[1]
    data['event_2_location'] = locations[1]
    data['event_2_description'] = descriptions[1]

  if event_count >= 3:
    data['event_3_name'] = name[2].text.strip()
    if len(src_list) > 3:
      data['event_3_image'] = src_list[3].strip()
    else:
      data['event_3_image'] = "static/assets/img/other/upcoming_event.png"
    data['event_3_start'] = starts[2]
    data['event_3_end'] = ends[2]
    data['event_3_location'] = locations[2]
    data['event_3_description'] = descriptions[2]

  json_file_path = "mps_site/static/event-data.json"

  with open(json_file_path, 'w') as json_file:
      json.dump(data, json_file, indent=4)
  