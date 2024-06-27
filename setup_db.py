import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mps.settings')
django.setup()

from mps_site.models import *

awards_list = [
    "Winner - Best Society in a Cultural/Academic/Social Field, DCU Society Awards 2024",
    "Winner - Society Personality - Shane O'Loughlin, DCU Society Awards 2024",
    "Winner - Individual Contribution to Society Life - Shane O'Loughlin, DCU Society Awards 2024",
    "Winner - Individual Contribution to Society Life - Sarah Ó Tuama, DCU Society Awards 2024",
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

dcufm_family_tree = [
    {"year": "2005/06 Manager", "name": "Sarah Dunne"},
    {"year": "2005/06 Programmes", "name": "Katie Galvin"},
    {"year": "2005/06 Tech Officer", "name": "Lizanna Barnwall"},
    {"year": "2006/07 Manager", "name": "Barry Bracken"},
    {"year": "2006/07 Programmes", "name": "Graeme Butler"},
    {"year": "2006/07 Tech Officer", "name": "Jack Fox"},
    {"year": "2008/09 Manager", "name": "Mark Moloney, Chris Cleary"},
    {"year": "2008/09 Programmes", "name": "Chris Cleary"},

    {"year": "2008/09 Tech Officer", "name": "Michaél Clesham"},
    {"year": "2009/10 Manager", "name": "Denis McEvoy"},
    {"year": "2009/10 Deputy", "name": "Alan Regan"},
    {"year": "2009/10 News Director", "name": "Steve Conlon"},
    {"year": "2010/11 Manager", "name": "Denis McEvoy"},
    {"year": "2010/11 Deputy", "name": "Vanessa Monaghan / Alan Regan"},
    {"year": "2011/12 Manager", "name": "Seamus Conwell"},
    {"year": "2011/12 Deputy", "name": "Russell James Alford"},

    {"year": "2012/13 Manager", "name": "Ciaran O'Connor"},
    {"year": "2012/13 Deputy", "name": "Cian McMahon"},
    {"year": "2013/14 Manager", "name": "Brian McLoughlin"},
    {"year": "2013/14 Deputy", "name": "James Shearer"},
    {"year": "2014/15 Manager", "name": "Sean Defoe"},
    {"year": "2014/15 Deputy", "name": "Eoin Sheahan"},
    {"year": "2015/16 Manager", "name": "Kevin Kelly"},
    {"year": "2015/16 Deputy", "name": "Caoimhe Ní Chathail"},

    {"year": "2016/17 Manager", "name": "Simon Doyle"},
    {"year": "2016/17 Deputy", "name": "Jaz Keane"},
    {"year": "2017/18 Manager", "name": "Jack Matthews"},
    {"year": "2017/18 Deputy", "name": "Sinéad Jordan"},
    {"year": "2018/19 Manager", "name": "Cathal O'Rourke"},
    {"year": "2018/19 Deputy", "name": "Dylan Mangan"},
    {"year": "2019/20 FM Manager", "name": "Éania McGarry"},
    {"year": "2019/20 FM Manager", "name": "Maeve Fortune"},
    
    {"year": "2020/21 FM Manager", "name": "Kate Burke"},
    {"year": "2020/21 FM Manager", "name": "Sarah McGuinness"},
    {"year": "2021/22 FM Manager", "name": "Sophie McDevitt"},
    {"year": "2021/22 FM Manager", "name": "Adam O'Dea"},
    {"year": "2022/23 FM Manager", "name": "Conor Smith"},
    {"year": "2022/23 FM Manager", "name": "Niall Walsh"},
    {"year": "2022/23 FM Manager", "name": "Kitty Leydon"},
    {"year": "2023/24 FM Manager", "name": "Caoimhe Woods"},
    {"year": "2023/24 FM Manager", "name": "Matthew Willis"},
    {"year": "2024/25 FM Manager", "name": "Lauren Joyce"},
    {"year": "2024/25 FM Manager", "name": "Eoin O'Sullivan"},
]

for award in awards_list:
    existing_award = Award.objects.filter(award_description=award).first()
    if not existing_award:
        new_award = Award(award_description=award)
        new_award.save()
        print(f"Award {award} added successfully.")
    else:
        print(f"Award {award} already exists.")

for member in dcufm_family_tree:
    existing_member = DCUfmFamilyTree.objects.filter(year=member["year"], name=member["name"]).first()
    if not existing_member:
        new_member = DCUfmFamilyTree(year=member["year"], name=member["name"])
        new_member.save()
        print(f"Member {member['name']} added successfully.")
    else:
        print(f"Member {member['name']} already exists.")