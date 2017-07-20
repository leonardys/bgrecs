import networkx as nx
import csv

G = nx.Graph()

with open('games.csv', 'r') as infile:
    reader = csv.DictReader(infile)

    for game in reader:
        # Print status
        print('Processing {}'.format(game['title']))

        traits = set(game['categories'].split(',') + game['mechanisms'].split(','))
        traits.discard('')

        # Add game into the graph
        G.add_node(game['id'], title=game['title'], traits=traits)

        # Link game with existing games based on shared traits
        for existing_game in G.nodes_iter():
            if existing_game == game['id']:
                continue

            for trait in iter(traits):
                if trait not in G.node[existing_game]['traits']:
                    continue

                if G.has_edge(game['id'], existing_game):
                    G[game['id']][existing_game]['weight'] += 1
                else:
                    G.add_edge(game['id'], existing_game, weight=1)

    # save the network
    nx.write_gexf(G, 'boardgame.gexf')
