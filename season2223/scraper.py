import requests
from bs4 import BeautifulSoup
import facebook
import instagram
import json

links = [
    'https://www.bfv.de/mannschaften/asv-moehrendorf/016PC46714000000VV0AG80NVV8OQVTB',
    'https://www.bfv.de/mannschaften/asv-moehrendorf-2/016PIHG3F4000000VV0AG811VUDIC8D7',
    'https://www.bfv.de/mannschaften/asv-moehrendorf-3/01P2DLNCJG000000VV0AG811VUH9CH7C'
]

for link in links:
    page = requests.get(link)
    soup = BeautifulSoup(page.content, "html.parser")
    next_match_link = soup.find_all("div", class_="bfv-result-tile")[1].find("a", recursive=False)['href']

    page = requests.get(next_match_link)
    soup = BeautifulSoup(page.content, "html.parser")

    # teams
    home = soup.find("div", class_="bfv-matchdata-result__team-name--team0").text.strip()
    team_home = 1
    if home[-4:] == " III":
        team_home = 3
        home = home.replace(' III', '')
    elif home[-3:] == " II":
        team_home = 2
        home = home.replace(' II', '')
    guest = soup.find("div", class_="bfv-matchdata-result__team-name--team1").text.strip()
    team_guest = 1
    if guest[-4:] == " III":
        team_guest = 3
        guest = guest.replace(' III', '')
    elif guest[-3:] == " II":
        team_guest = 2
        guest = guest.replace(' II', '')

    print(home, team_home)
    print(guest, team_guest)

    # date
    datetime = soup.find("div", class_="bfv-matchday-date-time").findAll("span", recursive=False)
    day = datetime[0].text[:-1]
    date = datetime[1].text.strip()[:10]
    time = datetime[1].text.strip()[-9:-4]

    # liga
    liga = soup.find("a", class_="bfv-link-heading").find("h3").text.split()[0]

    # ranks
    ranks = soup.find("div", class_="bfv-direktvergleich__data-entry")\
        .findAll("div", class_="bfv-direktvergleich-entry__data-text--basic")
    rank_home_team = int(ranks[0].text.strip())
    rank_guest_team = int(ranks[1].text.strip())

    with open('teams.json', 'r') as f:
        teams = json.load(f)

    facebook.create_facebook_image(
        home=teams[home],
        guest=teams[guest],
        team_home=team_home,
        team_guest=team_guest,
        rank_home=rank_home_team,
        rank_guest=rank_guest_team,
        date="{}, {}".format(day, date),
        time=time,
        liga=liga
    )
    instagram.create_instagram_image(
        home=teams[home],
        guest=teams[guest],
        team_home=team_home,
        team_guest=team_guest,
        rank_home=rank_home_team,
        rank_guest=rank_guest_team,
        date="{}, {}".format(day, date),
        time=time,
        liga=liga
    )
