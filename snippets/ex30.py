# %load ./snippets/ex30.py
def initial_state_Rvaccine(G): #vaccinate people randomly
    state = {}
    for node in G.nodes:
        state[node] = 'S'
    
    patient_zero = random.choice(list(G.nodes))
    state[patient_zero] = 'I'
    betwenness=pd.Series(dict(nx.betweenness_centrality(G))).sort_values(ascending=False)
    #target=betwenness.idxmax()
    #state[target]="R"
    targets=list(betwenness.index)[0:5]
    targets=rnd.sample(list(G.nodes), 5)
    for target in targets:
        state[target]="R"
    
    return state

def initial_state_Tvaccine(G):#targetted vaccination
    state = {}
    for node in G.nodes:
        state[node] = 'S'
    
    patient_zero = random.choice(list(G.nodes))
    state[patient_zero] = 'I'
    betwenness=pd.Series(dict(nx.betweenness_centrality(G))).sort_values(ascending=False)
    #target=betwenness.idxmax()
    #state[target]="R"
    targets=list(betwenness.index)[0:5]
    for target in targets:
        state[target]="R"
    
    return state


########
### Simulation
Nrep=100
repetitions = range(Nrep) 

########
### Simulation
Nrep=100
repetitions = range(Nrep) 

# Create the MultiIndex for the dataframe of storage
initial=["V","Control"]
multi_index = pd.MultiIndex.from_product([initial,repetitions], names=["Treatment","Repetition"])
#create dataframe
Infection_df=pd.DataFrame(index=multi_index, columns=["T_infec","N_infec"])

#run simulation for each model Nrep times and record consensus time
for start in initial:
    print(start)
    for nrep in range(Nrep):
        if (start=="Control"):
            test_state = initial_state_Rvaccine(G)
            sim = Simulation(G, test_state, state_transition, stop_condition_SI, name='SIR model')
            sim.run(200)
            T=sim.steps
            Infection_df.loc[(start,nrep),"T_infec"]=T
            value_counts = Counter(sim.state().values())
            Infection_df.loc[(start,nrep),"N_infec"]=value_counts["R"]

        else:
            test_state=initial_state_Tvaccine(G)
            sim = Simulation(G, test_state, state_transition, stop_condition_SI, name='SIR model')
            #sim.draw()
            sim.run(200)
            T=sim.steps
            Infection_df.loc[(start,nrep),"T_infec"]=T
            value_counts = Counter(sim.state().values())
            Infection_df.loc[(start,nrep),"N_infec"]=value_counts["R"]

            
        
        
Infection_df.groupby("Treatment").mean()