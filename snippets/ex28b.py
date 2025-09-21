
#### Simulation
Nrep=100
repetitions = range(Nrep) 

# Create the MultiIndex for the dataframe of storage
initial=["random","polarized"]
multi_index = pd.MultiIndex.from_product([ initial,repetitions], names=["start","Repetition"])
#create dataframe
Consensus_df=pd.DataFrame(index=multi_index, columns=["T_consensus"])

#run simulation for each model Nrep times and record consensus time
for start in initial:
    for nrep in range(Nrep):
        if (start=="random"):
            test_state = initial_state(G)
            sim = Simulation(G, test_state, state_transition, stop_condition, name='Voter model')
            sim.run(200)
            T=sim.steps
            Consensus_df.loc[(start,nrep),"T_consensus"]=T
        else:
            test_state=initial_state_polarized(G,group_state_dict, best_partition_map)
            sim = Simulation(G, test_state, state_transition, stop_condition, name='Voter model')
            #sim.draw()
            sim.run(200)
            T=sim.steps
            Consensus_df.loc[(start,nrep),"T_consensus"]=T
            
        
        
Consensus_df.groupby("start").mean()