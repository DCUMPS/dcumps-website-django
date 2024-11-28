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
    media_data = fetch_data(f"https://thecollegeview.ie/wp-json/wp/v2/media/{media_id}")
    return media_data['guid']['rendered'] if media_data else None

def tcv_posts(url):
    posts = fetch_data(url)
    if not posts:
        return []

    for post in posts:
        soup = BeautifulSoup(post['content']['rendered'], 'html.parser')
        post['content_plain'] = soup.get_text()
        first_image = soup.find('img')
        post['first_image'] = first_image['src'] if first_image else get_featured_media(post['featured_media'])
        
        post['formatted_date'] = datetime.strptime(post['date'], '%Y-%m-%dT%H:%M:%S').strftime('%B %d, %Y')

        author_data = fetch_data(f"https://thecollegeview.ie/wp-json/wp/v2/users/{post['author']}")
        if author_data:
            post['author_name'] = author_data.get('name')
            post['author_slug'] = author_data.get('slug')
        else:
            post['author_name'] = post['author_slug'] = None

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
    day_name = date.strftime("%A")
    hour = date.hour

    timetable = {
        "Monday": {
            9: "The X-Philes: Sinead Keane",
            10: "Tyler Murphy, Bethany Barrett, Zosia Kryszak",
            11: "Ciara Stell, Emily Mullally, Clodagh Mahon",
            12: "The Lunchtable: Aoife Hyland, Sé O’Reilly, Abbie Mahon Morrissey",
            13: "Newswire: Daniel Hayden and Grace Collins",
            14: "Action Replay: Eoin O'Sullivan and Mya Breen",
            15: "Ode to Youth: Debby Ugoiwa",
            16: "Perfecting perfection: Dearbhla McCormick, Aoibhín McEvoy",
            17: "Headlines, headlines, headlines: Adam Van Eekeren, Ester Pyykko",
            18: "Offside: Maxime Mancini",
            19: "No shows on at the moment",
            20: "Intrusive intruders: Angelina Zhao, Erin Reel",
        },
        "Tuesday": {
            9: "For the Plot: Leonor Selas Amaral, Shane Patrick Meleady, Lily Quinn",
            10: "Diabhal Scéal: Carla Reilly, Kate Rayel, Siobhra Behan",
            11: "Tipsy Tuesday: Jack Reynolds, Ronan Casey",
            12: "Kamil Kasza, Daire Canny, Anna Rzanek",
            13: "Dylan Hand, Ruby McManus, Alex Rowley",
            14: "Amelia O'Carroll, Essia Baouni, Leah Cahill",
            15: "Limelight: Lauren Joyce and Holly O'Neill",
            16: "The Dugout: Eoin O'Sullivan, Rian Lowry, Cian Mulligan, James Whittaker",
            17: "HerCampus Podcast: Lauren Joyce",
            18: "Eline Lund, Ceri Dunne, Marija Vasilonoka",
            19: "Unfocused: Eoin Murphy, Shane Codd",
            20: "Kle'epin it real: Gabby Klee",
        },
        "Wednesday": {
            9: "Journalism Away Days: Ciaran Kirk, Liam Rigley, Adam Balmer",
            10: "Dibs Boys: Matthew Willis, Finn McElwain, Luke Nolan",
            11: "Jake Dalton, Beth O’Connor, Shaney McConnon",
            12: "Tiarnán O’Kelly, Evan Dalton",
            13: "Fly on the wall: Katie Walsh, Holly Smith",
            14: "Cine Chat: Torna Mulconry, Dylan Hand",
            15: "Soundwaves: Sophie King, Sarah Duff",
            16: "Sabina Donnery, Emma Montalbani, Paddy Wanna",
            17: "The Morning debrief: Aoife Loughrey, Ella Geary, Katie Keating",
            18: "Football Fraudwatch: Matthew Joyce, Aaron Ingram",
            19: "The Football Show: Dylan Clarkin, Robert Curran",
            20: "Sound check",
        },
        "Thursday": {
            9: "Theme Machine: Daire Canny",
            10: "The Lore: Jane O’Reilly, Shelby Brennan, Molly McGurrin, Allyson Lambe",
            11: "Amy Caffrey, Shona Nugent, Kaitlyn Firmo",
            12: "Iara Moreira, Louise Akpofure, Aria Kazi",
            13: "PS talking BS: Sarah Murtagh, Patrycja Sykula",
            14: "This and Yap: Mya Breen, Olivia Doyle",
            15: "Crow talk: David Keyes, Rian Lowry, Rory Dalton, Sam Kennedy",
            16: "CinePop Chronicles: Sophie Egan and guests",
            17: "The SU Crew: Karl Ormsby, Aoife Butler, Brandon Perry, Alishaer Ahmed, Jamie Mangan",
            18: "Is this it?",
            19: "The Original Sin: Sam Murray, Douglas Murray",
            20: "Huge Jazz: Al Power, Michael Murphy, Tyler Murphy",
        },
        "Friday": {
            9: "Paddock to Pitch: Aimee Donnelly, Abby Whelan",
            10: "Hear us out: Dylan Tierney, Aine Foy, Sarah O’Donnell",
            11: "Ah Here!: Ava Shannon, Alyson Stewart, Georgia Ryan, Ella Verveen, Ellen McCahill",
            12: "Gossip girls: Zöe Percival, Kacey Matthews, Mia Mulvaney, Erin Miller",
            13: "Hot Girl Nonsense: Robyn Lawlor",
            14: "Congitive Dissonance: Éanna Kavanagh",
            15: "No shows on at the moment",
            16: "DCYou want the news? : Ailish Connor, Aaron Casey",
            17: "No shows on at the moment",
            18: "No shows on at the moment",
            19: "No shows on at the moment",
        }
    }

    if day_name in timetable and 9 <= hour <= 20:
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
    
def get_donation_count_fm():
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
                data['totalRaised'] = int(float(item.split(':')[1].replace('"', '')))
            if '"targetAmount":' in item:
                data['targetAmount'] = int(float(item.split(':')[1].replace('"', '')))
        
        return data
    
    except (requests.RequestException, ValueError, IndexError, AttributeError) as e:
        return data

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