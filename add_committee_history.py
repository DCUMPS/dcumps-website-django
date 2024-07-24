import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mps.settings')
django.setup()

from mps_site.models import *

CommitteeHistory.objects.all().delete()
CommitteeHistoryMember.objects.all().delete()

years = [
    "2017/18",
    "2018/19",
    "2019/20",
    "2020/21",
    "2021/22",
    "2022/23",
    "2023/24",
]

years = years[::-1]


for year in years:
    history = CommitteeHistory.objects.filter(year=year)
    if not history:
        CommitteeHistory.objects.create(year=year)
        print(f"Year {year} added to the database.")
    else:
        print(f"Year {year} already exists in the database.")


members = [
    {"year": "2023/24", "name": "Sarah O Tuama", "position": "Chairperson"},
    {"year": "2023/24", "name": "Jack Shannon-Nolan", "position": "Vice Chairperson"},
    {"year": "2023/24", "name": "Kate Byrne", "position": "Secretary"},
    {"year": "2023/24", "name": "Lauren Joyce", "position": "Treasurer"},
    {"year": "2023/24", "name": "Eabha Kelly", "position": "Public Relations Officer"},
    {"year": "2023/24", "name": "Liam O Keeffe", "position": "Brand Design Officer"},
    {"year": "2023/24", "name": "Hannah Daygo", "position": "Editor in Chief"},
    {"year": "2023/24", "name": "Laoise O Donnell Allen", "position": "Events Manager"},
    {"year": "2023/24", "name": "Sadhbh O Grady Keeley", "position": "Events Manager"},
    {"year": "2023/24", "name": "Caoimhe Woods", "position": "FM Manager"},
    {"year": "2023/24", "name": "Matthew Willis", "position": "FM Manager"},
    {"year": "2023/24", "name": "Adam Mulligan", "position": "Sponsorship Officer"},
    {"year": "2023/24", "name": "Shane O Loughlin", "position": "TV Manager"},
    {"year": "2023/24", "name": "Donal Mc Evoy", "position": "TV Manager"},
    {"year": "2023/24", "name": "Jake Farrell", "position": "Webmaster"},

    {"year": "2022/23", "name": "Adam O'Dea", "position": "Chairperson"},
    {"year": "2022/23", "name": "Becky Kelly", "position": "Vice Chairperson"},
    {"year": "2022/23", "name": "Eabha Kelly", "position": "Secretary"},
    {"year": "2022/23", "name": "Sophie Coleman", "position": "Treasurer"},
    {"year": "2022/23", "name": "Shane O Loughlin", "position": "Public Relations Officer"},
    {"year": "2022/23", "name": "Freya Kavanagh", "position": "Brand Design Officer"},
    {"year": "2022/23", "name": "Matthew Joyce", "position": "Editor-In-Chief, The College View"},
    {"year": "2022/23", "name": "Sarah O Tuama", "position": "Events Officer"},
    {"year": "2022/23", "name": "Jack Shannon-Nolan", "position": "Events Officer"},
    {"year": "2022/23", "name": "Conor Smith", "position": "FM Station Manager"},
    {"year": "2022/23", "name": "Niall Walsh", "position": "FM station manager"},
    {"year": "2022/23", "name": "Jack Collier", "position": "TV Manager"},
    {"year": "2022/23", "name": "Conor Daly", "position": "TV Manager"},
    {"year": "2022/23", "name": "Donal Mc Evoy", "position": "Webmaster"},

    {"year": "2021/22", "name": "Sarah Mc Guinness", "position": "Chairperson"},
    {"year": "2021/22", "name": "Ruairí Flynn", "position": "Vice Chair"},
    {"year": "2021/22", "name": "Kate Burke", "position": "Secretary"},
    {"year": "2021/22", "name": "Aisling Hurley", "position": "Treasurer"},
    {"year": "2021/22", "name": "Rachel Kiernan", "position": "Public Relations Officer"},
    {"year": "2021/22", "name": "Fionn O Leary", "position" : "Brand Design Officer"},
    {"year": "2021/22", "name": "Adam O'Dea", "position": "DCUfm station manager"},
    {"year": "2021/22", "name": "Katie Roache", "position": "Events Officer"},
    {"year": "2021/22", "name": "Muiris O'Cearbhaill", "position": "Events Officer"},
    {"year": "2021/22", "name": "Sophie Mc Devitt", "position": "FM Station Manager"},
    {"year": "2021/22", "name": "Daniel Breene", "position": "TV Manager"},
    {"year": "2021/22", "name": "Eoin O Reilly", "position": "TV Station Manager"},
    {"year": "2021/22", "name": "Gerard Shiels", "position": "Webmaster"},

    {"year": "2020/21", "name": "Maeve Fortune", "position": "Chairperson"},
    {"year": "2020/21", "name": "Andy", "position": "Secretary"},
    {"year": "2020/21", "name": "Jude Moran Nunn", "position": "Treasurer"},
    {"year": "2020/21", "name": "Gerard Shiels", "position": "Public Relations Officer"},
    {"year": "2020/21", "name": "Lara Walsh Fagherazzi", "position": "Brand Design Officer"},
    {"year": "2020/21", "name": "Sarah Mc Guinness", "position": "DCUfm station manager"},
    {"year": "2020/21", "name": "Kate Burke", "position": "DCUfm station manager"},
    {"year": "2020/21", "name": "Mark Moynihan", "position": "Events Officer"},
    {"year": "2020/21", "name": "Aoife O’Reilly", "position": "Events Officer"},
    {"year": "2020/21", "name": "Adam O'Dea", "position": "First-Year rep"},
    {"year": "2020/21", "name": "Ruairí Flynn", "position": "TV Manager"},
    {"year": "2020/21", "name": "Ciara Breslin", "position": "TV Manager"},
    {"year": "2020/21", "name": "Dylan Jacob Mc Clorey", "position": "Vice Chairperson"},
    {"year": "2020/21", "name": "Stephen Aherne", "position": "Webmaster"},

    {"year": "2019/20", "name": "Dylan Mango", "position": "Chairperson"},
    {"year": "2019/20", "name": "Cathal No Here", "position": "Vice Chairperson"},
    {"year": "2019/20", "name": "Kate O Grady", "position": "Secretary"},
    {"year": "2019/20", "name": "Walsh Robbie", "position": "Treasurer"},
    {"year": "2019/20", "name": "Neasa Monty", "position": "Public Relations Officer"},
    {"year": "2019/20", "name": "Gilleesagillen", "position": "Brand Design Officer"},
    {"year": "2019/20", "name": "Dylan McClorey", "position": "Events Manager"},
    {"year": "2019/20", "name": "Andy Vaughey", "position": "Deputy Events Manager"},
    {"year": "2019/20", "name": "_aoife_brady_", "position": "DCUtv Station Manager"},
    {"year": "2019/20", "name": "Neil Reilly", "position": "DCUtv Deputy Station Manager"},
    {"year": "2019/20", "name": "eaniamcgarry", "position": "DCUfm Station Manager"},
    {"year": "2019/20", "name": "maeve4tune", "position": "DCUfm Deputy Station Manager"},
    {"year": "2019/20", "name": "sarahsusanbrady98", "position": "Webmaster"},
    {"year": "2019/20", "name": "joshxmoff", "position": "First Year Rep"},

    {"year": "2018/19", "name": "Hannah Gallagher", "position": "Chairperson"},
    {"year": "2018/19", "name": "Aoife Horan", "position": "Treasurer"},
    {"year": "2018/19", "name": "Cathal O’Rourke", "position": "DCUfm Station Manager"},
    {"year": "2018/19", "name": "Robbie Walsh", "position": "Deputy Events Co-Ordinator"},
    {"year": "2018/19", "name": "Dylan McClorey", "position": "First-Year Rep"},
    {"year": "2018/19", "name": "Aoife McDermott", "position": "Vice Chairperson"},
    {"year": "2018/19", "name": "Ross McCarney", "position": "DCUtv Station Manager"},
    {"year": "2018/19", "name": "Dylan Mangan", "position": "Deputy DCUfm Station Manager"},
    {"year": "2018/19", "name": "Kate Gurren", "position": "Public Relations Officer"},
    {"year": "2018/19", "name": "Sarah Brady", "position": "Webmaster"},
    {"year": "2018/19", "name": "Sarah O’Dwyer", "position": "Secretary"},
    {"year": "2018/19", "name": "Eoin Cooke", "position": "Deputy DCUtv Station Manager"},
    {"year": "2018/19", "name": "Killian Whelan Mullally", "position": "Events Co-Ordinator"},
    {"year": "2018/19", "name": "Conor Doyle", "position": "Brand & Design Officer"},

    {"year": "2017/18", "name": "Billy Keenan", "position": "Chairperson"},
    {"year": "2017/18", "name": "Laura McKenna", "position": "Treasurer"},
    {"year": "2017/18", "name": "Jack Matthews", "position": "DCUfm Station Manager"},
    {"year": "2017/18", "name": "Carmel Kenny", "position": "Deputy Events Co-Ordinator"},
    {"year": "2017/18", "name": "Shane Barr", "position": "First-Year Rep"},
    {"year": "2017/18", "name": "Ciarán Harte", "position": "Vice Chairperson"},
    {"year": "2017/18", "name": "Aine Lawless", "position": "DCUtv Station Manager"},
    {"year": "2017/18", "name": "Sinead Jordan", "position": "Deputy DCUfm Station Manager"},
    {"year": "2017/18", "name": "Sarah O'Dwyer", "position": "Public Relations Officer"},
    {"year": "2017/18", "name": "Emily McEvoy", "position": "Secretary"},
    {"year": "2017/18", "name": "Hannah Gallagher", "position": "Deputy DCUtv Station Manager"},
    {"year": "2017/18", "name": "Aoife McDermott", "position": "Events Co-Ordinator"},
    {"year": "2017/18", "name": "Corey McLaughlin", "position": "Brand & Design Officer"},
]

for member in members:
    history = CommitteeHistory.objects.get(year=member["year"])
    if CommitteeHistoryMember.objects.filter(name=member["name"]).filter(position=member["position"]).first():
        print(f"Member {member['name']} already exists in the database.")
    else:
      new_member = CommitteeHistoryMember.objects.create(name=member["name"], position=member["position"])
      history.committee_members.add(new_member)
      print(f"Member {member['name']} added to the database.")