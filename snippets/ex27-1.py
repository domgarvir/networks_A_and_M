# Common parameters for the graphs
N=100
k=4 #number of neighbours
L=k*N #number of links
p=0.1 #probability of rewiring, for small world
m=L//(N-1) #scale free exponent , to have similar number of edges
# Set size of each community
community_sizes = [25, 25, 25,25]
community_probs =  np.array([[0.5, 0.01, 0.02,0.0], 
                   [0.01, 0.6, 0.05,0.0], 
                   [0.02, 0.05, 0.5,0.05],
                   [0.0 , 0.0 , 0.05, 0.5]])


net0=nx.gnm_random_graph(N,L,directed=False) #random
net1=nx.watts_strogatz_graph(N,k,0) #lattice
net2=nx.watts_strogatz_graph(N,k,p) #small-world
net3=nx.barabasi_albert_graph(N, m) #scale free
net4=nx.stochastic_block_model(community_sizes, community_probs*0.6) #SBM

#### Simulation
Nrep=100
repetitions = range(Nrep) 
models=["RND","REG","WS","BA","SBM"]
Networks={"REG":net1,"WS":net2,"BA":net3,"SBM":net4,"RND":net0}

# Create the MultiIndex for the dataframe of storage
multi_index = pd.MultiIndex.from_product([ models,repetitions], names=["Model","Repetition"])
#create dataframe
Consensus_df=pd.DataFrame(index=multi_index, columns=["T_consensus"])

#run simulation for each model Nrep times and record consensus time
for model in models:
    print(model, "\r")
    G=Networks[model]
    for nrep in range(Nrep):
        test_state = initial_state(G)
        sim = Simulation(G, initial_state, state_transition, stop_condition, name='Voter model')
        sim.run(200)
        T=sim.steps
        Consensus_df.loc[(model,nrep),"T_consensus"]=T
        

#see the consensus time of each model
Consensus_df.groupby("Model").mean().sort_values(by="T_consensus",ascending=True)