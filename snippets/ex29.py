from collections import Counter
net3=nx.barabasi_albert_graph(N, 3) #scale free
#### Simulation
Nrep=100
repetitions = range(Nrep) 

### Simulation
Nrep=100
repetitions = range(Nrep) 
models=["RND","BA"]
Networks={"REG":net1,"WS":net2,"BA":net3,"SBM":net4,"RND":net0}

# Create the MultiIndex for the dataframe of storage
multi_index = pd.MultiIndex.from_product([ models,repetitions], names=["Model","Repetition"])
#create dataframe
Infec_df=pd.DataFrame(index=multi_index, columns=["T_infec","N_infec"])

#run simulation for each model Nrep times and record consensus time
for model in models:
    print(model, "\r")
    G=Networks[model]
    for nrep in range(Nrep):
        test_state = initial_state(G)
        sim = Simulation(G, initial_state, state_transition, stop_condition_SI, name='SIR model')
        sim.run(200)
        T=sim.steps
        Infec_df.loc[(model,nrep),"T_infec"]=T
        value_counts = Counter(sim.state().values())
        Infec_df.loc[(model,nrep),"N_infec"]=value_counts["R"]

#see the consensus time of each model
Infec_df.groupby("Model").mean().sort_values(by="T_infec",ascending=True)