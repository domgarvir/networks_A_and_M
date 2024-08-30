connected=nx.is_connected(Bnet)

#if network is connected then obtain the sets with the coloring algorithm
if connected:
    bottom_nodes, top_nodes = bipartite.sets(Bnet)
else:
    top_nodes = {n for n, d in Bnet.nodes(data=True) if d["bipartite"] == 0}
    bottom_nodes = set(Bnet) - top_nodes
    
print(top_nodes)
print(bottom_nodes)