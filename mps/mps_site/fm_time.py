import datetime
import time

def get_date_time():
    date = datetime.datetime.now()
    day_of_week = date.weekday() + 1  # Adjusting to match the JavaScript day index (1-7)
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

if __name__ == "__main__":
    while True:
        previous, current, next_show = get_date_time()
        print(f"Previous Show: {previous}")
        print(f"Current Show: {current}")
        print(f"Next Show: {next_show}")
        time.sleep(1)
