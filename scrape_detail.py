# Read list of games from a csv file
# Get categories and mechanisms for each game
# Save the details to a csv file
import requests
import csv
from lxml import etree

api_url = 'https://www.boardgamegeek.com/xmlapi/boardgame/{}'
batch_size = 100

# Read games list
with open('games.csv', 'r') as infile, open('detail.csv', 'w') as outfile:
    # Skip header
    reader = csv.reader(infile)
    next(reader)

    writer = csv.writer(outfile)
    writer.writerow(['title', 'categories', 'mechanics'])

    batch = []

    for i, game in enumerate(reader):
        # Print status
        print('Scraping {} ({})'.format(game[1], i+1))

        batch.append(game[0])

        if len(batch) < batch_size:
            continue

        # Get XML
        page = requests.get(api_url.format(','.join(batch))).text
        doc = etree.fromstring(page)

        # Process each game data
        for game_node in doc.getchildren():
            # Get categories and mechanisms
            name = game_node.findall('name[@primary]')[0].text
            categories = ','.join([category.text for category in game_node.findall('boardgamecategory')])
            mechanics = ','.join([mechanic.text for mechanic in game_node.findall('boardgamemechanic')])

            # Write data to the csv file
            writer.writerow([name, categories, mechanics])

        batch = []
