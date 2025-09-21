#1. Read the file and sotre in dataframe
Idf=pd.read_csv(filename, header=0, index_col=0)
#print(Idf.head())

#2. Create bipartite network
# Initialize an empty bipartite graph
B = nx.Graph()
# Add producers (rows) and consumers (columns) as nodes
plants = Idf.index
animals = Idf.columns

# Add nodes with a bipartite identifier
B.add_nodes_from(plants, bipartite="plant")  # Set for producers
B.add_nodes_from(animals, bipartite="animal")  # Set for consumers
# Add edges for non-zero interactions, we can also use the matrix directly
for plant in plants:
    for animal in animals:
        if Idf.loc[plant, animal] != 0:
            B.add_edge(plant, animal)

#3. Get the number of nodes in each set an the number of links
Nplants=len(plants)
Nanimals=len(animals)
L=B.number_of_edges()
print("Np=%s Na=%s, L=%s" %(Nplants,Nanimals,L))

# 4. Generate the random version of the network
B_R1=bipartite.gnmk_random_graph(Nplants, Nanimals, L)
# to force that the graph uses bipartite="plant" or bipartite="animal" instead of the o and 1 by default we can do:
for n in range(Nplants):
    B_R1.nodes[n]["bipartite"]="plant"
for n in range(Nplants,Nplants+Nanimals):
    B_R1.nodes[n]["bipartite"]="animal"