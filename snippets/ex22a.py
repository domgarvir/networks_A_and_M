Nrep = 3  # Replace this with your desired number of repetitions
repetitions = range(Nrep + 1)  # Repetition numbers from 0 to Nrep
ensembles = ["ER", "KSEQ"]  # Ensemble names
metrics = ["S1", "S2","S3","S4","S5"]  # Metric names to asses

# Create the MultiIndex
multi_index = pd.MultiIndex.from_product([repetitions, ensembles], names=["Repetition", "Ensemble"])

# Create an empty DataFrame with this MultiIndex
Value_df = pd.DataFrame(index=multi_index, columns=metrics)   

###############################################
#prepare parameters for null models
N=FW.number_of_nodes()
L=FW.number_of_edges()
Kin=pd.Series(dict(FW.in_degree))
Kout=pd.Series(dict(FW.out_degree))

#########################################################
Motifs_empirical=pd.Series(mcounter_py3(FW,motifs), name="EMP") #get empirical values

#Noew let's fill the dataframe
for rep in range(5):
    print(rep, "\r")
    #generate the randomization in first null model
    FW_ER=nx.gnm_random_graph(N, L,directed=True)
    Motifs_ER=pd.Series(mcounter_py3(FW_ER,motifs), name="RND_1")
    Value_df.loc[(rep,"ER"), : ]= Motifs_ER
    
    
    FW_R3=randomization_constant_Kseq(FW, directed=True)
    Motifs_R3=pd.Series(mcounter_py3(FW_R3,motifs), name="RND_3")
    Value_df.loc[(rep,"KSEQ"), : ]= Motifs_R3
    
Value_df.head()