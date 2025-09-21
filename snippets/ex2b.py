 # One mode networks connect two nodes in the same set (let's say people) with as many links as shared partners they have in the second set (parties).
    
#In our case, George and Paul have been only in new year party, however, George and Jhon have been in two aprties togheter: new year and summer solstice!

WG = nx.Graph()

weighted_edges=[("Paul", "John",1), ("Paul", "George",1),("John", "Richard",2),("John", "George",2), ("George", "Richard",1)] #a lis ofweighted edges, weight represent the number of shared parties
WG.add_weighted_edges_from(weighted_edges) #add the list of edges to the network

#now let's plot it
pos=nx.spring_layout(WG) # we need to get the position of the nodes to after add the node labels
nx.draw_networkx(WG,pos,node_color="skyblue",node_size=1000)
w = nx.get_edge_attributes(WG,'weight') #get the edge attribute ẁeigth'
nx.draw_networkx_edges(G = WG, pos = pos, edge_color='k', width=list(w.values())) #representing the weigth tih the thickness of the link
#nx.draw_networkx_edge_labels(G,pos,edge_labels=labels) #if you wat to see the weigth
plt.show()