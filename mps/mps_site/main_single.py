#!/usr/bin/python3


import requests 
from bs4 import BeautifulSoup 
from PIL import Image, ImageDraw, ImageFont
import datetime
import time
import random
import sys
import os

def create_donation_thermometer(goal, current_donation, image_width=400, image_height=700):
    # Create a blank image with RGBA color mode (4 channels including Alpha)
    image = Image.new("RGBA", (image_width, image_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)

    # Set font and size
    font_path = "GaretHeavy.ttf"
    font = ImageFont.truetype(font_path, size=50)
    #font = ImageFont.load_default()

    # Define colors
    border_color = (255, 255, 255)
    #mercury_color = (166, 229, 228) - TV
    mercury_color = (149, 239, 185) # - FM
    #mercury_color = (166, 229, 228, 128)  # Set alpha to 128 for semi-transparency

    # Draw border
    #draw.rectangle([(0, 0), (image_width - 1, image_height - 1)], outline=border_color)

    # Draw thermometer outline
    border_width = 10
    fixed_image_height = 700
    thermometer_width = 90
    draw.rectangle([(image_width // 2 - thermometer_width // 2, 250), (image_width // 2 + thermometer_width // 2, fixed_image_height - 100)], outline=border_color, width=border_width)

    # Calculate mercury height based on current donation and goal
    max_thermometer_height = image_height
    bar_height = current_donation
    if current_donation >= goal:
        bar_height = goal
    #print("350")
    mercury_height = (int((bar_height / goal) * max_thermometer_height)) / 2
    #print(mercury_height)

    # Draw mercury
    mercury_top = fixed_image_height - 95 - mercury_height + border_width
    mercury_bottom = fixed_image_height - 105 - border_width  # Adjust the offset as needed
    mercury_left = image_width // 2 - thermometer_width // 2 + 5 + border_width
    mercury_right = image_width // 2 + thermometer_width // 2 - 5 - border_width
    draw.rectangle([(mercury_left, mercury_top), (mercury_right, mercury_bottom)], fill=mercury_color)

    # Draw text
    #text = f"Donation Progress: ${current_donation} / ${goal}"
    text = f"{current_donation} / {goal}"
    text_width, text_height = draw.textsize(text, font)
    draw.text(((image_width - text_width) // 2, fixed_image_height - 70), text, font=font, fill=(255, 255, 255))
    text = f"DONATION\nPROGRESS"
    text_width, text_height = draw.textsize(text, font)
    draw.text(((image_width - text_width) // 2, fixed_image_height - 600), text, font=font, fill=(255, 255, 255))

    return image

# Example usage
#goal_amount = 10000
#current_donation_amount = int(input("Enter the current donation amount, Example: 1234 (No Decimals): "))
#current_donation_amount = 1000
# thermometer_image = create_donation_thermometer(goal_amount, current_donation_amount)
# thermometer_image.save("donation_thermometer.png")
# every 5-10 minutes
def get_donation_count_fm():
    URL = "https://www.idonate.ie/fundraiser/MediaProductionSociety11"
    headers = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0"} 
    r = requests.get(url=URL, headers=headers) 
    soup = BeautifulSoup(r.content, 'html5lib')
    current_donation = soup.find('div', attrs = {'class':'ifs-right-fundraisers-head'}) 
    donation_target = soup.find('div', attrs = {'class':'support-cause'}) 
    current_donation_amount = int(str(current_donation).split()[3].split("€")[1].split("<")[0].replace(",",""))
    goal_amount = int(str(donation_target).split("€")[1].split("<")[0].replace(",",""))
    thermometer_image = create_donation_thermometer(goal_amount, current_donation_amount)
    thermometer_image.save("./mps_site/static/donation_thermometer.png")
    cropped_image = Image.open("./mps_site/static/donation_thermometer.png")
    cropped_image = cropped_image.crop((0, 110, 400, 700))
    cropped_image.save("./mps_site/static/donation_thermometer.png")
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Donation Count Updated ({current_time}): €{current_donation_amount} out of €{goal_amount}")

if __name__ == "__main__":
    get_donation_count_fm()