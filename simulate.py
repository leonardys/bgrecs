import networkx as nx

# Load network
G = nx.read_gml('boardgame.gml')

# Rating
#  2 = I really like it
#  1 = I like it
#  0 = No preference
# -1 = I don't like it
# -2 = I really don't like it
nx.set_node_attributes(G, 'rating', 0)
nx.set_node_attributes(G, 'rated', False)

# Functions
def rate(node, rating=0, rated=True):
    alpha = 0.01
    epsilon = 0.001

    # Set node rating
    G.node[node]['rating'] = rating
    G.node[node]['rated'] = rated

    # Process neighbors
    for neighbor in G.neighbors_iter(node):
        # Skip user-rated game
        if G.node[neighbor]['rated']:
            continue

        change = alpha * ((G.node[node]['rating'] * G.edge[node][neighbor]['weight'] / G.node[node]['ntrait']) - G.node[neighbor]['rating'])

        if abs(change) > epsilon:
            neighbor_value = G.node[neighbor]['rating'] + change
            rate(neighbor, rating=neighbor_value, rated=False)

def top_like(n=10):
    return sorted([G.node[node] for node in G.nodes()], key=lambda x: x['rating'], reverse=True)[:n]

def top_dislike(n=10):
    return sorted([G.node[node] for node in G.nodes()], key=lambda x: x['rating'])[:n]
