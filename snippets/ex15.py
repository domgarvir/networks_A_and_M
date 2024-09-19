#Read the Incidence matrix
filename="./data/WoL_Tronqueira/tronqueira.csv"
Idf=pd.read_csv(filename, header=0, index_col=0)
#print(Idf.head()) #allways print wath you import!!!!!
Idf=Idf.drop("Number of droppings analysed\"", axis=0)

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

            #since the function takes the matrix lets convert the network to amtrix form
Amat_T = nx.to_pandas_adjacency(B) #get full adjacency matrix
Imat_T = Amat_T.loc[list(plants), list(animals)] #subselect the A vs P interactions

eta_T=nestedness2(Imat_T)
Q_T=nx.community.modularity(B,nx.community.louvain_communities(B))


#modularity of the other network:
Q=nx.community.modularity(B1,nx.community.louvain_communities(B1))

plt.plot([eta, eta_T],[Q,Q_T],'.')
plt.xlabel("nestedness")
plt.ylabel("modularity")