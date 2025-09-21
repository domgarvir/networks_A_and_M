B2=nx.Graph()
#add books
books=["B1","B2","B3","B4","B5"]
#add attribute bipartite
B2.add_nodes_from(books, bipartite="book")
#for each book, search in the book graph for the existing edges
for i in range(5):
    nodes=graphs[i].nodes()
    for node in nodes:
        B2.add_edge(books[i],node) #associate the edge with the book in the new network
        
#don't forget to give the new nodes the bipartite attribute
character_nodes = set(B2) - set(books)
for node in int_nodes:
     B2.nodes[node]["bipartite"]="int"
        
#book projections
book_projection = nx.bipartite.weighted_projected_graph(B2, books)
Books_df=nx.to_pandas_adjacency(book_projection)
Books_df