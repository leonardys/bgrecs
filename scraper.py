import requests
import csv
from lxml import html, etree

base = 'https://boardgamegeek.com'
list_url = '/browse/boardgame'
detail_url = '/xmlapi/boardgame/'
last_page = False

with open('games.csv', 'w') as outfile:
    writer = csv.writer(outfile)
    writer.writerow(['id', 'title', 'rating', 'num_voters', 'categories', 'mechanisms'])

    while not last_page:
        # Print status
        print('Scraping {}'.format(base+list_url))

        # Get page content
        html_page = requests.get(base+list_url).text
        html_doc = html.fromstring(html_page)

        # Get list of games and write them to the csv file
        game_list = html_doc.cssselect('td.collection_objectname a')
        game_ids = [game.attrib['href'].split('/')[-2] for game in game_list]
        ratings = iter(html_doc.cssselect('td.collection_bggrating'))

        # Get detail
        xml_page = requests.get(base+detail_url+','.join(game_ids)).text
        xml_doc = etree.fromstring(xml_page)

        # Process each game data
        for id, game_node, _, rating, num_voters in zip(game_ids, xml_doc.getchildren(), ratings, ratings, ratings):
            # Get categories and mechanisms
            title = game_node.findall('name[@primary]')[0].text
            categories = ','.join([category.text for category in game_node.findall('boardgamecategory')])
            mechanics = ','.join([mechanic.text for mechanic in game_node.findall('boardgamemechanic')])

            # Write data to the csv file
            writer.writerow([id, title, rating.text.strip(), num_voters.text.strip(), categories, mechanics])

        # Check next page link
        link = html_doc.cssselect('#collection+p a')[-2]
        list_url = link.attrib['href']

        if "Next" not in link.text_content():
            last_page = True
