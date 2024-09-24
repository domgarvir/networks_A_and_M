filename="./data/pollination/Herrera_Donana.csv"
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

            
Nrep = 100  # Replace this with your desired number of repetitions
repetitions = range(Nrep + 1)  # Repetition numbers from 0 to Nrep
ensembles = ["ER", "CONF","KSEQ"]  # Ensemble names
metrics = ["eta"]  # Metric names to asses

# Create the MultiIndex
# Create the MultiIndex
multi_index = pd.MultiIndex.from_product([repetitions, ensembles], names=["Repetition", "Ensemble"])

# Create an empty DataFrame with this MultiIndex
Value_df = pd.DataFrame(index=multi_index, columns=metrics)   

##############################################
#prepare parameters for null models
#3. Get the number of nodes in each set an the number of links
Nplants=len(plants)
Nanimals=len(animals)
L=B.number_of_edges()
Ka=pd.Series(dict(B.degree(animals))).sort_values(ascending=False)
Kp=pd.Series(dict(B.degree(plants))).sort_values(ascending=False)
print("Np=%s Na=%s, L=%s" %(Nplants,Nanimals,L))

#########################################################
bottom_nodes = {n for n, d in B.nodes(data=True) if d["bipartite"] == "plant"}#get nodes with bipartite==0
eta_emp=nestedness_bipartite(B,bottom_nodes)
print(eta_emp)

#Noew let's fill the dataframe
for rep in range(Nrep+1):
    # 4. Generate the random version of the network
    B_R1=bipartite.gnmk_random_graph(Nplants, Nanimals, L)
    # to force that the graph uses bipartite="plant" or bipartite="animal" instead of the o and 1 by default we can do:
    for n in range(Nplants):
        B_R1.nodes[n]["bipartite"]="plant"
    for n in range(Nplants,Nplants+Nanimals):
        B_R1.nodes[n]["bipartite"]="animal"
        
    bottom_nodesR = {n for n, d in B_R1.nodes(data=True) if d["bipartite"] == "plant"}#get nodes with bipartite==0
    eta_R1=nestedness_bipartite(B_R1,bottom_nodesR)
    Value_df.loc[(rep,"ER"), "eta"]= eta_R1
    
    B_R2=bipartite.configuration_model(Kp,Ka)
    # to force that the graph uses bipartite="plant" or bipartite="animal" instead of the o and 1 by default we can do:
    for n in range(Nplants):
        B_R2.nodes[n]["bipartite"]="plant"
    for n in range(Nplants,Nplants+Nanimals):
        B_R2.nodes[n]["bipartite"]="animal"
    
    bottom_nodesR = {n for n, d in B_R2.nodes(data=True) if d["bipartite"] == "plant"}#get nodes with bipartite==0
    eta_R2=nestedness_bipartite(B_R2,bottom_nodesR)
    Value_df.loc[(rep,"CONF"), "eta"]= eta_R2
    #print(eta_R2)
    
    bottom_nodes = {n for n, d in B.nodes(data=True) if d["bipartite"] == "plant"}#get nodes with bipartite==0
    top_nodes = set(B) - bottom_nodes

    #create the randomized version
    B_R3=randomization_constant_Kseq_bipart(B,bottom_nodes,top_nodes)
    #we need to specify the bottom nodes to get nestedness
    bottom_nodesR = {n for n, d in B_R3.nodes(data=True) if d["bipartite"] == "plant"}#get nodes with bipartite==0
    eta_R3=nestedness_bipartite(B_R3,bottom_nodesR)
    Value_df.loc[(rep,"KSEQ"), "eta"]= eta_R3
    #print(eta_R3)
    
Value_df.head()