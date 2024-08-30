G = nx.Graph()
nodes_to_add = [1, 2, 3, 4, 5]
G.add_nodes_from(nodes_to_add)
edges_to_add = [(1, 2), (2,3), (3,4), (3,5)]
G.add_edges_from(edges_to_add)
nx.draw(G, with_labels=True)