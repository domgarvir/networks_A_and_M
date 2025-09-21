# 4. Generate the random version of the network
Nplants=len(plants)
Nanimals=len(animals)
L=B.number_of_edges()

B_R1=bipartite.gnmk_random_graph(Nplants, Nanimals , L)
# to force that the graph uses bipartite="plant" or bipartite="animal" instead of the o and 1 by default we can do:
for n in range(Nplants):
    B_R1.nodes[n]["bipartite"]="plant"
for n in range(Nplants,Nplants+Nanimals):
    B_R1.nodes[n]["bipartite"]="animal"

#Create mappings for renaming
plant_mapping = {i: plants[i] for i in range(Nplants)}
pollinator_mapping = {i + Nplants: animals[i] for i in range(Nanimals)}

# Combine the mappings
mapping = {**plant_mapping, **pollinator_mapping}

# Relabel the nodes in the bipartite graph
B_R1 = nx.relabel_nodes(B_R1, mapping)

################
SurvR1_df=pd.DataFrame(index=np.arange(N_sim),  columns=list(A)) #create dataframe to store results

rho=0.005 
delta=0.0
gamma_avg=0.1

ImatR1=nx.to_pandas_adjacency(B_R1).loc[animals, plants]
matricesR1=interaction_matrix(ImatR1, gamma_avg = gamma_avg, rho = rho, delta = delta)
AR1=matricesR1["alpha"]#this is the matrix of itneractions among all species
#r=simplex_sampling(1,len(A)) #sample reproductive rates randomly in the unit sphere, we reuse the same as before!

#run the simulation
for sim in range(N_sim):
    ri=r[sim]
    N_sol = np.linalg.inv(AR1) @ r[sim].reshape(-1, 1) #solve the system of equations
    psurvivors=[0 if i<0 else 1 for i in N_sol]
    SurvR1_df.iloc[sim]=psurvivors
    
#######
((SurvR1_df.sum()/N_sim)).hist(alpha=0.8,label="RND")
((Surv_df.sum()/N_sim)).hist(alpha=0.8, label="EMP")
plt.xlabel("Presence")
plt.ylabel("P(presence)")
plt.legend()
plt.show()