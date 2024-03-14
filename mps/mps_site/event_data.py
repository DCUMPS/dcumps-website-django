#!/usr/bin/env python3

import requests 
from bs4 import BeautifulSoup     
import json

def get_event_data():

  #URL = "https://dcuclubsandsocs.ie/society/engineering"
  #URL = "https://dcuclubsandsocs.ie/society/islamic"
  #URL = "https://dcuclubsandsocs.ie/society/redbrick"
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

  json_file_path = "mps_site/event-data.json"
  #json_file_path = "event-data.json"

  # Write the data to the JSON file
  with open(json_file_path, 'w') as json_file:
      json.dump(data, json_file, indent=4)

  print(f"Data has been written to {json_file_path}")


if __name__ == "__main__":
  get_event_data()
  print("Event data has been updated.")
  