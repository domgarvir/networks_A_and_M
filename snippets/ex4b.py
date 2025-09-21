   # Weighted projection where weights represent the number of parties attended together
people_projection = nx.bipartite.weighted_projected_graph(Bparty, people)

#now let's plot it
pos=nx.spring_layout(people_projection) # we need to get the position of the nodes to after add the node labels
nx.draw_networkx(people_projection,pos,node_color="skyblue",node_size=1000)
w = nx.get_edge_attributes(people_projection,'weight') #get the edge attribute ẁeigth'
nx.draw_networkx_edges(G = people_projection, pos = pos, edge_color='k', width=list(w.values())) #representing the weigth tih the thickness of the link
#nx.draw_networkx_edge_labels(G,pos,edge_labels=labels) #if you wat to see the weigth
plt.show()

# Print the edges in the one-mode network with their weights
print("One-mode projection of people (edges and weights):")
for u, v, weight in people_projection.edges(data='weight'):
    print(f"{u} - {v}: {weight} parties together")