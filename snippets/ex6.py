#Read the Incidence matrix
filename="./data/WoL_Tronqueira/tronqueira.csv"
Idf=pd.read_csv(filename, header=0, index_col=0)
print(Idf.head()) #allways print wath you import!!!!!
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

# Now B is your bipartite network
#print("Nodes:", B.nodes)
#print("Edges:", B.edges)

pos = nx.bipartite_layout(B, animals) #assing position to the nodes acoording to their bipartite property
color_dict={"plant":"red","animal":"blue"} #dictionary of node color, each bipartite set is asociated to a different color
colors = [color_dict[node[1]['bipartite']] for node in B.nodes(data=True)]
nx.draw(B, pos, node_color=colors, with_labels=True)