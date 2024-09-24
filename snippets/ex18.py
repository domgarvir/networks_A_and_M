#read the edgelist and create the network
filename="./data/WoL_StMarks/st_marks_Ilist.csv"
Ilist=pd.read_csv(filename, header=None, index_col=None)
Ilist.columns=["source","target","w"]
FW=nx.from_pandas_edgelist(Ilist, edge_attr="w", create_using=nx.DiGraph)

#The null model that keeps fixed the number of nodes and links is the gnm model. We need to know how many species and how many links there are:
N=nx.number_of_nodes(FW)
L=nx.number_of_edges(FW)
print(N,L)
FW_R1 = nx.gnm_random_graph(N, L, directed=True)
print(nx.number_of_nodes(FW_R1),nx.number_of_edges(FW_R1)) #just to be sure