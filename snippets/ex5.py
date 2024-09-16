#read the matrix of interaction and store it in the dataframe
filename="./data/WoL_StMarks/st_marks.csv"
Idf=pd.read_csv(filename, header=0, index_col=0)

#probably you will try:
#DG=nx.from_pandas_adjacency(Idf,create_using=nx.DiGraph)
#but it returs an error because it only works for SQUARE matrices!!
#We need to find a better way:

#Since no all species are in the rows and the columns, the default method does NOT work, is better to take this approach:
G = nx.DiGraph()

# Use the stack() function to create a series, and then filter out zeros
edges = Idf.stack().reset_index()
edges = edges[edges[0] != 0]  # Filter out non-interactions (zeros)

# Adding edges to the directed graph
G.add_edges_from(zip(edges['level_0'], edges['level_1']))

# Print nodes and edges to verify
#print("Nodes:", G.nodes)
#print("Edges:", G.edges)

nx.draw(G, with_labels=True)