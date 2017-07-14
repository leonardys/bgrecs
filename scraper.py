import requests
import csv
from lxml import html

base = 'https://boardgamegeek.com'
url = '/browse/boardgame'
games = {}
last_page = False

while not last_page:
    # Get and page content
    page = requests.get(base+url).text
    doc = html.fromstring(page)

    # Get list of games
    game_list = doc.cssselect('td.collection_objectname a')
    for game in game_list:
        id = game.attrib['href'].split('/')[-2]
        title = game.text_content()
        games[id] = title

    # Check next page link
    link = doc.cssselect('#collection+p a')[-2]
    url = link.attrib['href']

    if "Next" not in link.text_content():
        last_page = True

# Export games to csv
with open('games.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['id', 'title'])
    for game in games.items():
        writer.writerow(game)
