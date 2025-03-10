import csv
import networkx as nx
from itertools import combinations

G = nx.Graph()
groups = {}

with open('games.csv', 'r') as infile:
    reader = csv.DictReader(infile)

    for game in reader:
        id = int(game['id'])
        title = game['title']
        try:
            num_voters = int(game['num_voters'])
        except:
            num_voters = 0
        traits = set(game['categories'].split(',') + game['mechanisms'].split(','))
        traits.discard('')

        # Skip expansions and games that have no traits or have less than 500 voters
        if len(traits) == 0 or num_voters < 500 or 'Expansion for Base-game' in traits:
            continue

        # Print status
        print('Processing {}'.format(title))

        # Add game into the graph
        G.add_node(id, {'label': title, 'ntrait': len(traits), 'rating': 0.0, 'rated': False})

        # Group similar games based on traits
        for trait in iter(traits):
            try:
                groups[trait].append(id)
            except:
                groups[trait] = [id]

for trait, games in iter(groups.items()):
    # Print status
    print('Processing {}'.format(trait))

    for source, target in combinations(games, 2):
        if G.has_edge(source, target):
            G[source][target]['weight'] += 1
        else:
            G.add_edge(source, target, weight=1)

# Save the network
nx.write_gexf(G, 'boardgame.gexf')
