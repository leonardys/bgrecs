# Read list of games from a csv file
# Get categories and mechanisms for each game
# Save the details to a csv file
import requests
import csv
from lxml import etree

api_url = 'https://www.boardgamegeek.com/xmlapi/boardgame/{}'

# Read games list
with open('games.csv', 'r') as infile, open('detail.csv', 'w') as outfile:
    # Skip header
    reader = csv.reader(infile)
    next(reader)

    writer = csv.writer(outfile)
    writer.writerow(['title', 'categories', 'mechanics'])

    for i, game in enumerate(reader):
        # Print status
        print('Scraping {} ({})'.format(game[1], i+1))

        # Get XML
        page = requests.get(api_url.format(game[0])).text
        doc = etree.fromstring(page)

        # Get categories and mechanisms
        categories = ','.join([category.text for category in doc.getchildren()[0].findall('boardgamecategory')])
        mechanics = ','.join([mechanic.text for mechanic in doc.getchildren()[0].findall('boardgamemechanic')])

        # Write data to the csv file
        writer.writerow([game[1], categories, mechanics])
