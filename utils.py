import networkx as nx

# Rate a game
def rate(G, node, rating, alpha=1e-2, epsilon=5e-3, max_iters=1e6):
    num_iters = 0

    # Set node rating
    G.node[node]['rating'] = float(rating)
    G.node[node]['rated'] = 1

    queue = set([(node, neighbor) for neighbor in G.neighbors(node)])

    while len(queue) and num_iters < max_iters:
        num_iters += 1
        source, target = queue.pop()

        # Skip if both source and target are user-rated
        if G.node[source]['rated'] and G.node[target]['rated']:
            continue

        if G.node[target]['rated']:
            queue.add((target, source))
            continue

        change = alpha * ((G.node[source]['rating'] * G.edge[source][target]['weight'] / G.node[source]['ntrait']) - G.node[target]['rating'])

        if abs(change) > epsilon:
            G.node[target]['rating'] += change
            queue = queue.union({(target, neighbor) for neighbor in G.neighbors(target)})

def top_likes(G, n=10):
    return sorted([G.node[node] for node in G.nodes() if not G.node[node]['rated']], key=lambda x: x['rating'], reverse=True)[:n]

def top_dislikes(G, n=10):
    return sorted([G.node[node] for node in G.nodes() if not G.node[node]['rated']], key=lambda x: x['rating'])[:n]

def rated_games(G):
    return sorted([G.node[node] for node in G.nodes() if G.node[node]['rated']], key=lambda x: x['rating'], reverse=True)

def save_subset(G, filename):
    subset = [node for node in G.nodes() if G.node[node]['rated'] == True or G.node[node]['rating'] != 0]
    H = G.subgraph(subset)
    nx.write_gexf(H, filename)
