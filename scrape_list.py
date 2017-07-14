# Get list of games from https://boardgamegeek.com/browse/boardgame
# Save the list to a csv file
import requests
import csv
from lxml import html

base = 'https://boardgamegeek.com'
url = '/browse/boardgame'
last_page = False

with open('games.csv', 'w') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(['id', 'title'])

    while not last_page:
        # Print status
        print('Scraping {}'.format(base+url))

        # Get page content
        page = requests.get(base+url).text
        doc = html.fromstring(page)

        # Get list of games and write them to the csv file
        game_list = doc.cssselect('td.collection_objectname a')
        for game in game_list:
            id = game.attrib['href'].split('/')[-2]
            title = game.text_content()
            writer.writerow([id, title])

        # Check next page link
        link = doc.cssselect('#collection+p a')[-2]
        url = link.attrib['href']

        if "Next" not in link.text_content():
            last_page = True
