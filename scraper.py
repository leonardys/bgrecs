import requests
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
        name = game.text_content()
        games[id] = name

    # Check next page link
    link = doc.cssselect('#collection+p a')[-2]
    url = link.attrib['href']

    if "Next" not in link.text_content():
        last_page = True
