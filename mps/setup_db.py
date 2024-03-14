import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mps.settings')
django.setup()

from mps_site.models import Award

awards_list = [
    "Winner - Best Society Promotional Video, 2023 Board of Irish College Society Awards 2023",
    "Winner - Best Society Publicity Campaign - DCUtv 24hr Broadcast, DCU Society Awards 2023",
    "Winner - Best Society Promotional Video - Welcome to MPS '22/23, DCU Society Awards 2023",
    "Winner - Individual Contribution to Society Life - Jack Collier, DCU Society Awards 2023",
    "Winner - Best Charitable Contribution - (society), DCU Society Awards 2021",
    "Winner - Best Society Poster - DCUfm 12hr Broadcast, DCU Society Awards 2021",
    "Winner - Individual Contribution to Society Life - Ciara Breslin, DCU Society Awards 2021",
    "Winner - Best Society in Ireland - Board of Irish College Society Awards 2015",
    "Winner - Best Society Event - DCUtv 24hr Broadcast , DCU Society Awards 2014",
    "Winner - Best Society, DCU Society Awards 2013",
    "Winner - Best Online Presence 2012, The Board of Irish College Society Awards 2012",
    "Winner - Best Communication & Marketing 2012, DCU Society Awards 2012",
    "Winner - Best College Society in Ireland 2011, The Board of Irish College Society Awards 2011",
]

for award in awards_list:
    existing_award = Award.objects.filter(award_description=award).first()
    if not existing_award:
        new_award = Award(award_description=award)
        new_award.save()
        print(f"Award {award} added successfully.")
    else:
        print(f"Award {award} already exists.")
