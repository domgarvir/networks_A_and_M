#start creating an empty graph
B=nx.Graph()
#add books
books=["B1","B2","B3","B4","B5"]
#add attribute bipartite
B.add_nodes_from(books, bipartite="book")
#for each book, search in the book graph for the existing edges
for i in range(5):
    edges=graphs[i].edges()
    for edge in edges:
        B.add_edge(books[i],edge) #associate the edge with the book in the new network
        
#don't forget to give the new nodes the bipartite attribute
int_nodes = set(B) - set(books)
for node in int_nodes:
     B.nodes[node]["bipartite"]="int"
        
#book projections
book_projection = nx.bipartite.weighted_projected_graph(B, books)
Books_df=nx.to_pandas_adjacency(book_projection)
Books_df