import requests
from bs4 import BeautifulSoup
from . import facebook_event, story, square
import json
import os
from datetime import datetime as dt
from enum import Enum
import babel.dates

class SOCIAL_MEDIA(Enum):
	FB_EVENT = facebook_event
	STORY = story
	SQUARE = square


def create_image(platform: SOCIAL_MEDIA, team: int):
	assert 0 < team < 3
	links = [
		'https://www.bfv.de/mannschaften/asv-moehrendorf/016PC46714000000VV0AG80NVV8OQVTB',
		'https://www.bfv.de/mannschaften/asv-moehrendorf-2/016PIHG3F4000000VV0AG811VUDIC8D7',
	]
	link = links[team-1]

	page = requests.get(link)
	soup = BeautifulSoup(page.content, "html.parser")
	next_match_link = soup.find_all("div", class_="bfv-result-tile")[1].find("a", recursive=False)['href']

	page = requests.get(next_match_link)
	soup = BeautifulSoup(page.content, "html.parser")

	# teams
	home = soup.find("div", class_="bfv-matchdata-result__team-name--team0").text.strip()

	team_home = 1
	if home[-2:] == " 2":
		team_home = 2
		home = home.replace(' 2', '')
	if home[-3:] == " II":
		team_home = 2
		home = home.replace(' II', '')
	guest = soup.find("div", class_="bfv-matchdata-result__team-name--team1").text.strip()
	team_guest = 1
	if guest[-2:] == " 2":
		team_guest = 2
		guest = guest.replace(' 2', '')
	if guest[-3:] == " II":
		team_guest = 2
		guest = guest.replace(' II', '')

	# print(home, team_home)
	# print(guest, team_guest)

	# date
	datetime = soup.find("div", class_="bfv-matchday-date-time").findAll("span", recursive=False)
	date_str = datetime[1].text.strip()[:10]
	time_str = datetime[1].text.strip()[-9:-4]
	d = dt.strptime(f"{date_str}T{time_str}", '%d.%m.%YT%H:%M')
	# locale.setlocale(locale.LC_TIME, "de_DE")
	# date = d.strftime("%A, %d. %B")
	# time = d.strftime("%H:%M")
	date = babel.dates.format_datetime(d, "EEEE, d. MMMM", locale="de_DE")
	time = babel.dates.format_time(d, "H:mm", locale="de_DE")

	# liga
	liga = soup.find("a", class_="bfv-link-heading").find("h3").text.split()[0]

	# ranks
	# ranks = soup.find("div", class_="bfv-direktvergleich__data-entry")\
		# .findAll("div", class_="bfv-direktvergleich-entry__data-text--basic")
	rank_home_team = 1 # int(ranks[0].text.strip())
	rank_guest_team = 2 # int(ranks[1].text.strip())

	with open(os.path.abspath(os.path.dirname(__file__)) + '/teams.json', 'r', encoding='utf-8') as f:
		teams = json.load(f)

	return platform.value.create_image(
		home=teams[home],
		guest=teams[guest],
		team_home=team_home,
		team_guest=team_guest,
		rank_home=rank_home_team,
		rank_guest=rank_guest_team,
		date=date,
		time=time,
		liga=liga
	)
